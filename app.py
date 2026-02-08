import logging
import sys
from datetime import datetime
from flask import Flask, render_template, jsonify, request

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

@app.before_request
def log_request():
    logger.info(
        "request_start path=%s method=%s remote_addr=%s",
        request.path,
        request.method,
        request.remote_addr,
    )

@app.after_request
def log_response(response):
    logger.info(
        "request_end path=%s status=%s",
        request.path,
        response.status_code,
    )
    return response

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
    """
    Lightweight health-check endpoint.

    Intended for:
    - Render health checks
    - External uptime monitoring
    - Debugging deployment issues
    """
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
