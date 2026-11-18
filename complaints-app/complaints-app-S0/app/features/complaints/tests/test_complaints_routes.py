"""Tests for the complaints home page."""

from app.config import TestConfig
from app.features.complaints import repository


def test_home_page_returns_200(client):
    assert client.get("/").status_code == 200


def test_home_page_lists_every_sample_complaint(client):
    html = client.get("/").get_data(as_text=True)
    complaints = repository.list_complaints()
    assert complaints
    for complaint in complaints:
        assert complaint.reference in html
        assert complaint.complainant_name in html


def test_home_page_shows_status_as_text(client):
    html = client.get("/").get_data(as_text=True)
    for label in ("Logged", "Investigating", "Pending approval", "Approved", "Closed"):
        assert label in html


def test_home_page_shows_prototype_banner(client):
    html = client.get("/").get_data(as_text=True)
    assert TestConfig.PROTOTYPE_BANNER in html


def test_home_page_is_responsive_and_semantic(client):
    html = client.get("/").get_data(as_text=True)
    assert 'name="viewport"' in html
    assert "table-responsive" in html
    assert "<main" in html
    assert 'scope="col"' in html


def test_home_page_pins_bootstrap_version(client):
    html = client.get("/").get_data(as_text=True)
    assert "bootstrap@5.3." in html
    assert "@latest" not in html


def test_home_page_rejects_post(client):
    assert client.post("/").status_code == 405
