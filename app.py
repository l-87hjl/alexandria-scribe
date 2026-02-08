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

            if ext == ZIP_EXT:
                with zipfile.ZipFile(f) as zf:
                    for name in zf.namelist():
                        raw = zf.read(name)
                        inner = secure_filename(os.path.basename(name))
                        inner_ext = "." + inner.split(".")[-1].lower() if "." in inner else ""

                        if inner_ext == PDF_EXT:
                            for frag in extract_pdf_fragments(raw, f"{filename}:{inner}"):
                                add_fragment(
                                    content=frag["content"],
                                    source=frag["source"],
                                    source_type="pdf",
                                    source_page=frag["source_page"],
                                )
                                ingested += 1
                            continue

                        if inner_ext == DOCX_EXT:
                            for frag in extract_docx_fragments(raw, f"{filename}:{inner}"):
                                add_fragment(
                                    content=frag["content"],
                                    source=frag["source"],
                                    source_type="docx",
                                )
                                ingested += 1
                            continue

                        if inner_ext in ALLOWED_TEXT_EXTS:
                            add_fragment(
                                content=raw.decode("utf-8", errors="ignore"),
                                source=f"{filename}:{inner}",
                                source_type="text",
                            )
                            ingested += 1
                        else:
                            skipped += 1
                continue

            if ext == PDF_EXT:
                raw = f.read()
                for frag in extract_pdf_fragments(raw, filename):
                    add_fragment(
                        content=frag["content"],
                        source=filename,
                        source_type="pdf",
                        source_page=frag["source_page"],
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

# (rest of file unchanged)
