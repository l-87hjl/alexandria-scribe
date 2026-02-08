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
from werkzeug.exceptions import HTTPException

from storage import init_db, add_fragment, list_fragments, search_fragments
from similarity import compute_similarity
from recombulator import fetch_fragments_by_ids, assemble_markdown, assemble_text, assemble_zip
from pdf_ingestion import extract_pdf_fragments
from docx_ingestion import extract_docx_fragments

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("alexandria_scribe")

app = Flask(__name__, template_folder="templates")
init_db()

PAGE_SIZE = 25
ALLOWED_TEXT_EXTS = {".txt", ".md", ".csv"}
ZIP_EXT = ".zip"
PDF_EXT = ".pdf"
DOCX_EXT = ".docx"

@app.before_request
def log_request_start():
    g.start_time = time.perf_counter()
    logger.info("request_start path=%s method=%s", request.path, request.method)

@app.after_request
def log_request_end(response):
    duration_ms = (time.perf_counter() - g.start_time) * 1000
    logger.info("request_end path=%s status=%s duration_ms=%.2f", request.path, response.status_code, duration_ms)
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    tb = traceback.format_exc()
    logger.error("unhandled_exception %s\n%s", repr(e), tb)
    return jsonify({"error": "internal_server_error"}), 500

# ---------------- Landing ----------------
@app.route("/")
def landing():
    return render_template("landing.html")

# ---------------- Disassembler ----------------
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

            if ext == PDF_EXT:
                raw = f.read()
                for frag in extract_pdf_fragments(raw, filename):
                    add_fragment(
                        content=frag["content"],
                        source=filename,
                        source_type="pdf",
                        source_page=frag.get("source_page"),
                    )
                    ingested += 1
                continue

            if ext == DOCX_EXT:
                raw = f.read()
                for frag in extract_docx_fragments(raw, filename):
                    add_fragment(
                        content=frag["content"],
                        source=filename,
                        source_type="docx",
                    )
                    ingested += 1
                continue

            if ext in ALLOWED_TEXT_EXTS:
                raw = f.read()
                add_fragment(
                    content=raw.decode("utf-8", errors="ignore"),
                    source=filename,
                    source_type="text",
                )
                ingested += 1
            else:
                skipped += 1

        logger.info("ingestion_complete ingested=%s skipped=%s", ingested, skipped)
        return redirect(url_for("fragments"))

    return render_template("disassembler.html")

# ---------------- Fragment Browser ----------------
@app.route("/fragments", methods=["GET"])
def fragments():
    query = request.args.get("q", "").strip()
    page = max(int(request.args.get("page", 1)), 1)
    offset = (page - 1) * PAGE_SIZE

    if query:
        rows = search_fragments(query=query, limit=PAGE_SIZE, offset=offset)
    else:
        rows = list_fragments(limit=PAGE_SIZE, offset=offset)

    return render_template(
        "fragments.html",
        fragments=rows,
        query=query,
        page=page,
    )

# ---------------- Recombulator ----------------
@app.route("/recombulator", methods=["GET", "POST"])
def recombulator():
    if request.method == "POST":
        ids = [int(x) for x in request.form.getlist("fragment_ids") if x.isdigit()]
        fmt = request.form.get("format", "zip")
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

# ---------------- Health ----------------
@app.route("/health")
def health():
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info("Starting Alexandria-Scribe on port %s", port)
    app.run(host="0.0.0.0", port=port)
