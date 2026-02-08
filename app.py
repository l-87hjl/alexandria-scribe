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

@app.route("/health")
def health():
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()})

# --- Disassembler, fragments, recombulator routes unchanged ---

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info("Starting Alexandria-Scribe on port %s", port)
    app.run(host="0.0.0.0", port=port)
