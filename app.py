import logging
import sys
import time
import traceback
from datetime import datetime
from io import BytesIO
import zipfile
import tempfile
import os
from flask import Flask, render_template, jsonify, request, g, redirect, url_for, send_file
from werkzeug.utils import secure_filename

from storage import init_db, add_fragment, list_fragments, search_fragments
from similarity import compute_similarity
from recombulator import fetch_fragments_by_ids, assemble_markdown, assemble_text, assemble_zip

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

# Allowed ingestion types (Stage 1: text only)
ALLOWED_TEXT_EXTS = {".txt", ".md", ".csv"}
ZIP_EXT = ".zip"

# Safety limits
MAX_ZIP_FILES = 500
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB per file

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

# ----------------------------
# Global Error Handling
# ----------------------------
@app.errorhandler(Exception)
def handle_exception(e):
    duration_ms = None
    if hasattr(g, "start_time"):
        duration_ms = (time.perf_counter() - g.start_time) * 1000

    tb = traceback.format_exc()

    logger.error(
        "unhandled_exception path=%s method=%s duration_ms=%s error=%s\n%s",
        request.path,
        request.method,
        f"{duration_ms:.2f}" if duration_ms is not None else "-1",
        repr(e),
        tb,
    )

    response = {
        "error": "internal_server_error",
        "message": "An unexpected error occurred. Check server logs for details.",
    }
    return jsonify(response), 500

# ----------------------------
# Helper: process a single text file
# ----------------------------

def ingest_text_file(raw_bytes: bytes, filename: str):
    try:
        text = raw_bytes.decode("utf-8", errors="ignore").strip()
    except Exception:
        return False

    if not text:
        return False

    add_fragment(content=text, source=filename)
    return True

# ----------------------------
# Routes
# ----------------------------
@app.route("/")
def landing():
    return render_template("landing.html")

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

            # ----- ZIP ingestion -----
            if ext == ZIP_EXT:
                try:
                    with zipfile.ZipFile(f) as zf:
                        names = zf.namelist()[:MAX_ZIP_FILES]
                        for name in names:
                            if name.endswith("/"):
                                continue

                            inner_name = secure_filename(os.path.basename(name))
                            inner_ext = "." + inner_name.split(".")[-1].lower() if "." in inner_name else ""

                            if inner_ext not in ALLOWED_TEXT_EXTS:
                                skipped += 1
                                continue

                            info = zf.getinfo(name)
                            if info.file_size > MAX_FILE_SIZE_BYTES:
                                skipped += 1
                                continue

                            raw = zf.read(name)
                            if ingest_text_file(raw, f"{filename}:{inner_name}"):
                                ingested += 1
                            else:
                                skipped += 1
                except zipfile.BadZipFile:
                    logger.info("ingest_skip bad_zip filename=%s", filename)
                    skipped += 1
                continue

            # ----- Plain text ingestion -----
            if ext not in ALLOWED_TEXT_EXTS:
                skipped += 1
                continue

            raw = f.read(MAX_FILE_SIZE_BYTES + 1)
            if len(raw) > MAX_FILE_SIZE_BYTES:
                skipped += 1
                continue

            if ingest_text_file(raw, filename):
                ingested += 1
            else:
                skipped += 1

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

        try:
            ids = [int(x) for x in ids]
        except ValueError:
            ids = []

        fragments = fetch_fragments_by_ids(ids)

        if not fragments:
            return jsonify({"error": "no_fragments_selected"}), 400

        if fmt == "zip":
            buf = assemble_zip(fragments)
            logger.info("recombulator_export ids=%s format=zip", ids)
            return send_file(
                buf,
                as_attachment=True,
                download_name="recombined_fragments.zip",
                mimetype="application/zip",
            )

        if fmt == "txt":
            content = assemble_text(fragments)
            filename = "recombined_fragments.txt"
            mimetype = "text/plain"
        else:
            content = assemble_markdown(fragments)
            filename = "recombined_fragments.md"
            mimetype = "text/markdown"

        logger.info("recombulator_export ids=%s format=%s", ids, fmt)

        return send_file(
            BytesIO(content.encode("utf-8")),
            as_attachment=True,
            download_name=filename,
            mimetype=mimetype,
        )

    return render_template("recombulator.html")

@app.route("/health")
def health():
    payload = {
        "status": "ok",
        "service": "alexandria-scribe",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    logger.info("health_check")
    return jsonify(payload), 200


if __name__ == "__main__":
    logger.info("starting alexandria-scribe application")
    app.run(host="0.0.0.0", port=5000)
