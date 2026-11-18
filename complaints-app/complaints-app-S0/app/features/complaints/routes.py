"""Routes for the complaints feature. Routes only render; logic is in services."""

from flask import Blueprint, render_template

from app.features.complaints import services

bp = Blueprint("complaints", __name__, template_folder="templates")


@bp.get("/")
def index():
    """Show the sample complaints list. Temporary: S1 puts this behind login."""
    return render_template(
        "complaints/index.html", rows=services.list_complaint_rows()
    )
