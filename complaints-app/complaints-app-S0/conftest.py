"""Shared pytest fixtures, available to cross-cutting and feature tests."""

import pytest

from app import create_app
from app.config import TestConfig


@pytest.fixture
def app():
    """A fresh application using TestConfig."""
    return create_app(TestConfig)


@pytest.fixture
def client(app):
    """A test client for the application."""
    return app.test_client()
