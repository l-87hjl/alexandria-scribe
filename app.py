import logging
import sys
import time
import traceback
from datetime import datetime
from flask import Flask, render_template, jsonify, request, g

from storage import init_db

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
# Routes
# ----------------------------
@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/disassembler")
def disassembler():
    return render_template("disassembler.html")

@app.route("/fragments")
def fragments():
    return render_template("fragments.html")

@app.route("/recombulator")
def recombulator():
    return render_template("recombulator.html")

# ----------------------------
# Health / Heartbeat
# ----------------------------
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
