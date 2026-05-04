# ai-service/app.py

import logging
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from pathlib import Path

# Load environmen
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

#  Flask app
app = Flask(__name__)

# Rate limiter — 30 requests/min
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["30 per minute"],
    headers_enabled=True,
)

# Health check
@app.route("/health", methods=["GET"])
def health():
    logger.info("Health check called")
    return jsonify({
        "status":  "ok",
        "service": "ai-service",
        "port":    5000
    }), 200

#  Error handlers
@app.errorhandler(400)
def bad_request(e):
    return jsonify({
        "error":   "Bad request",
        "message": str(e),
        "status":  400
    }), 400

@app.errorhandler(404)
def not_found(e):
    logger.warning(f"Endpoint not found — {str(e)}")
    return jsonify({
        "error":   "Not found",
        "message": "The requested endpoint does not exist",
        "status":  404
    }), 404

@app.errorhandler(405)
def method_not_allowed(e):
    logger.warning(f"Method not allowed — {str(e)}")
    return jsonify({
        "error":   "Method not allowed",
        "message": "Check your HTTP method — GET/POST/PUT/DELETE",
        "status":  405
    }), 405

@app.errorhandler(422)
def unprocessable_entity(e):
    logger.warning(f"Unprocessable entity — {str(e)}")
    return jsonify({
        "error":   "Unprocessable entity",
        "message": "Request body is valid JSON but contains invalid fields",
        "status":  422
    }), 422

@app.errorhandler(429)
def rate_limit_exceeded(e):
    logger.warning(f"Rate limit exceeded — {str(e)}")
    return jsonify({
        "error":   "Too many requests",
        "message": "Maximum 30 requests per minute allowed",
        "status":  429
    }), 429

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error — {str(e)}")
    return jsonify({
        "error":   "Internal server error",
        "message": "Something went wrong on the AI service",
        "status":  500
    }), 500

# Register blueprints
from routes.describe  import describe_bp
from routes.recommend import recommend_bp
from routes.generate_report import generate_report_bp

app.register_blueprint(describe_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(generate_report_bp)

#  Entry point
if __name__ == "__main__":
    logger.info("Starting AI service on port 5000")
    app.run(host="0.0.0.0", port=5000, debug=False)