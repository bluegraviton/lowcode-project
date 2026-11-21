"""Cross-cutting rule: GET requests do not change the data (Build Plan 8.3.5)."""

import copy

from app import sample_data
from app.features.complaints import repository


def get_routes_without_arguments(app) -> list[str]:
    return sorted(
        rule.rule
        for rule in app.url_map.iter_rules()
        if "GET" in rule.methods and not rule.arguments
    )


def test_get_requests_do_not_change_the_data(app, client):
    paths = get_routes_without_arguments(app)
    assert "/" in paths and "/health" in paths

    raw_before = copy.deepcopy((sample_data.USERS, sample_data.COMPLAINTS))
    records_before = repository.list_complaints()

    for path in paths:
        assert client.get(path).status_code == 200

    assert (sample_data.USERS, sample_data.COMPLAINTS) == raw_before
    assert repository.list_complaints() == records_before


def test_every_get_route_is_covered(app):
    # Flask's built-in static route takes a path argument; it serves files only.
    uncovered = sorted(
        rule.rule
        for rule in app.url_map.iter_rules()
        if "GET" in rule.methods and rule.arguments and rule.endpoint != "static"
    )
    assert uncovered == [], (
        "GET routes with path parameters are not exercised by the no-write "
        f"test; extend it before adding them: {uncovered}"
    )
