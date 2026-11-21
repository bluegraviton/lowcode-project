"""Health feature: a minimal status endpoint that exposes no data."""

from flask import Flask

from app.features.health.routes import bp


def register(app: Flask) -> None:
    """Register the health blueprint on the app."""
    app.register_blueprint(bp)
