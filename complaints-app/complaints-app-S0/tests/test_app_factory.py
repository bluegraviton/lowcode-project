"""Cross-cutting checks on the application factory and FEATURES list."""

from pathlib import Path

from app import FEATURES, create_app
from app.config import Config, TestConfig

FEATURES_DIR = Path(__file__).resolve().parent.parent / "app" / "features"


def feature_name(module) -> str:
    return module.__name__.rsplit(".", 1)[-1]


def test_factory_registers_every_feature(app):
    for feature in FEATURES:
        assert feature_name(feature) in app.blueprints


def test_every_feature_folder_is_in_the_features_list():
    folders = {
        p.name
        for p in FEATURES_DIR.iterdir()
        if p.is_dir() and (p / "__init__.py").exists()
    }
    assert folders == {feature_name(f) for f in FEATURES}


def test_factory_uses_the_given_config():
    assert create_app(TestConfig).config["TESTING"] is True
    assert create_app(Config).config["TESTING"] is False


def test_factory_returns_independent_apps():
    assert create_app(TestConfig) is not create_app(TestConfig)
