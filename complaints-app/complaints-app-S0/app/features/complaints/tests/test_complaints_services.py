"""Tests for the complaints service."""

from app.config import CATEGORY_LABELS, PRODUCT_LABELS, STATUS_LABELS
from app.features.complaints import repository, services


def test_one_row_per_complaint():
    assert len(services.list_complaint_rows()) == len(repository.list_complaints())


def test_rows_use_display_labels_not_raw_values():
    for row in services.list_complaint_rows():
        assert row.product_label in PRODUCT_LABELS.values()
        assert row.category_label in CATEGORY_LABELS.values()
        assert row.status_label in STATUS_LABELS.values()


def test_rows_are_most_recently_received_first():
    dates = [row.received_date for row in services.list_complaint_rows()]
    assert dates == sorted(dates, reverse=True)
