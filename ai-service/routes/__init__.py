from __future__ import annotations

from flask import Flask

from routes.describe import describe_bp
from routes.health import health_bp
from routes.recommend import recommend_bp
from routes.report import report_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(health_bp)
    app.register_blueprint(describe_bp)
    app.register_blueprint(recommend_bp)
    app.register_blueprint(report_bp)
