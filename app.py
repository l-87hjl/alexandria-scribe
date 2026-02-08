import logging
import sys
import time
import traceback
from datetime import datetime
from io import BytesIO
import zipfile
import os
from flask import Flask, render_template, jsonify, request, g, redirect, url_for, send_file
from werkzeug.utils import secure_filename

from storage import init_db, add_fragment, list_fragments, search_fragments
from similarity import compute_similarity
from recombulator import fetch_fragments_by_ids, assemble_markdown, assemble_text, assemble_zip
from pdf_ingestion import extract_pdf_fragments

# ----------------------------
# Logging Configuration
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("alexandria_scribe")

# ----------------------------
# App Setup
# ----------------------------
app = Flask(__name__, template_folder="templates")

# Initialize persistent storage on startup
init_db()
logger.info("fragment_store_initialized")

# Pagination defaults
PAGE_SIZE = 25

# Allowed ingestion types (Stage 1)
ALLOWED_TEXT_EXTS = {".txt", ".md", ".csv"}
ZIP_EXT = ".zip"
PDF_EXT = ".pdf"

# Safety limits
MAX_ZIP_FILES = 500
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024

@app.before_request
def log_request_start():
    g.start_time = time.perf_counter()
    logger.info(
        "request_start path=%s method=%s remote_addr=%s",
        request.path,
        request.method,
        request.remote_addr,
    )

@app.after_request
def log_request_end(response):
    duration_ms = None
    if hasattr(g, "start_time"):
        duration_ms = (time.perf_counter() - g.start_time) * 1000

    logger.info(
        "request_end path=%s status=%s duration_ms=%.2f",
        request.path,
        response.status_code,
        duration_ms if duration_ms is not None else -1,
    )
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    tb = traceback.format_exc()
    logger.error("unhandled_exception %s\n%s", repr(e), tb)
    return jsonify({"error": "internal_server_error"}), 500

# ----------------------------
# Routes
# ----------------------------
@app.route("/disassembler", methods=["GET", "POST"])
def disassembler():
    if request.method == "POST":
        files = request.files.getlist("files")
        ingested = 0
        skipped = 0

        for f in files:
            if not f or not f.filename:
                continue

            filename = secure_filename(f.filename)
            ext = "." + filename.split(".")[-1].lower() if "." in filename else ""

            # ZIP ingestion (already supported)
            if ext == ZIP_EXT:
                try:
                    with zipfile.ZipFile(f) as zf:
                        for name in zf.namelist()[:MAX_ZIP_FILES]:
                            if name.endswith("/"):
                                continue
                            inner_name = secure_filename(os.path.basename(name))
                            inner_ext = "." + inner_name.split(".")[-1].lower() if "." in inner_name else ""
                            raw = zf.read(name)

                            if inner_ext == PDF_EXT:
                                fragments = extract_pdf_fragments(raw, f"{filename}:{inner_name}")
                                for frag in fragments:
                                    add_fragment(content=frag["content"], source=f"{frag['source']}#page{frag['source_page']}")
                                    ingested += 1
                                continue

                            if inner_ext not in ALLOWED_TEXT_EXTS:
                                skipped += 1
                                continue

                            add_fragment(content=raw.decode("utf-8", errors="ignore"), source=f"{filename}:{inner_name}")
                            ingested += 1
                except zipfile.BadZipFile:
                    skipped += 1
                continue

            # Direct PDF ingestion
            if ext == PDF_EXT:
                raw = f.read(MAX_FILE_SIZE_BYTES * 10)
                fragments = extract_pdf_fragments(raw, filename)
                for frag in fragments:
                    add_fragment(content=frag["content"], source=f"{filename}#page{frag['source_page']}")
                    ingested += 1
                continue

            # Plain text ingestion
            if ext not in ALLOWED_TEXT_EXTS:
                skipped += 1
                continue

            raw = f.read(MAX_FILE_SIZE_BYTES)
            add_fragment(content=raw.decode("utf-8", errors="ignore"), source=filename)
            ingested += 1

        logger.info("ingestion_complete ingested=%s skipped=%s", ingested, skipped)
        return redirect(url_for("fragments"))

    return render_template("disassembler.html")

@app.route("/fragments", methods=["GET"])
def fragments():
    query = request.args.get("q", "").strip()
    page = max(int(request.args.get("page", 1)), 1)
    offset = (page - 1) * PAGE_SIZE

    if query:
        rows = search_fragments(query=query, limit=PAGE_SIZE, offset=offset)
    else:
        rows = list_fragments(limit=PAGE_SIZE, offset=offset)

    fragment_pairs = [(row["id"], row["content"]) for row in rows]
    similarity = compute_similarity(fragment_pairs)

    return render_template(
        "fragments.html",
        fragments=rows,
        similarity=similarity,
        query=query,
        page=page,
    )

@app.route("/recombulator", methods=["GET", "POST"])
def recombulator():
    if request.method == "POST":
        ids = request.form.getlist("fragment_ids")
        fmt = request.form.get("format", "md")
        ids = [int(x) for x in ids if x.isdigit()]
        fragments = fetch_fragments_by_ids(ids)

        if fmt == "zip":
            return send_file(
                assemble_zip(fragments),
                as_attachment=True,
                download_name="recombined_fragments.zip",
                mimetype="application/zip",
            )

        content = assemble_text(fragments) if fmt == "txt" else assemble_markdown(fragments)
        return send_file(
            BytesIO(content.encode("utf-8")),
            as_attachment=True,
            download_name=f"recombined_fragments.{fmt}",
        )

    return render_template("recombulator.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
