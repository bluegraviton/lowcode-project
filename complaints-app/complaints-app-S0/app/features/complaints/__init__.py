"""Complaints feature: the sample complaints list (temporary until S1)."""

from flask import Flask

from app.features.complaints.routes import bp


def register(app: Flask) -> None:
    """Register the complaints blueprint on the app."""
    app.register_blueprint(bp)
