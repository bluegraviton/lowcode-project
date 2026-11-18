"""Tests for the health feature."""


def test_health_returns_ok_json(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"status": "ok"}


def test_health_exposes_no_data(client):
    body = client.get("/health").get_data(as_text=True)
    assert "CMP-" not in body
    assert "example.com" not in body


def test_health_rejects_non_get_methods(client):
    assert client.post("/health").status_code == 405
