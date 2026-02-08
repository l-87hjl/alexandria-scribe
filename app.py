import os
import logging
from flask import Flask, request, render_template, redirect, url_for

from storage import init_db, add_fragment, list_fragments
from ingestion import ingest_files

app = Flask(__name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@app.before_first_request
def startup():
    init_db()
    logger.info("Database initialized")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/disassembler", methods=["GET", "POST"])
def disassembler():
    if request.method == "POST":
        files = request.files.getlist("files")
        fragment_count = 0
        file_count = 0

        if files:
            result = ingest_files(files)
            fragment_count = result.get("fragment_count", 0)
            file_count = result.get("file_count", 0)

        logger.info(
            "Ingestion complete: %s fragments from %s files",
            fragment_count,
            file_count,
        )

        return render_template(
            "ingestion_complete.html",
            fragment_count=fragment_count,
            file_count=file_count,
        )

    return render_template("disassembler.html")

@app.route("/fragments")
def fragments():
    q = request.args.get("q")
    page = int(request.args.get("page", 1))
    fragments = list_fragments(query=q, page=page)
    return render_template("fragments.html", fragments=fragments, page=page)

@app.route("/export/all")
def export_all():
    format = request.args.get("format", "zip")
    return export_all_fragments(format=format)

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info("Starting Alexandria Scribe on port %s", port)
    app.run(host="0.0.0.0", port=port)
