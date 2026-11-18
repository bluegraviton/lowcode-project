"""Complaints App application factory."""

from flask import Flask

from app.config import Config
from app.features import complaints, health

# The single place features are registered. Adding a feature means one new
# folder under app/features plus one line here.
FEATURES = [
    health,
    complaints,
]


def create_app(config_class: type = Config) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    for feature in FEATURES:
        feature.register(app)
    return app
