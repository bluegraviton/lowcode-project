"""Routes for the health feature."""

from flask import Blueprint, jsonify

bp = Blueprint("health", __name__)


@bp.get("/health")
def health():
    """Return a minimal status response. Reads and writes no data."""
    return jsonify(status="ok")
