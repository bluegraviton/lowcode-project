"""Tests for the complaints service."""

from app.config import CATEGORY_LABELS, PRODUCT_LABELS, STATUS_LABELS
from app.features.complaints import repository, services


def test_one_row_per_complaint():
    assert len(services.list_complaint_rows()) == len(repository.list_complaints())


def test_each_row_shows_the_labels_for_its_own_complaint():
    rows_by_reference = {row.reference: row for row in services.list_complaint_rows()}

    for complaint in repository.list_complaints():
        row = rows_by_reference[complaint.reference]
        assert row.product_label == PRODUCT_LABELS[complaint.product]
        assert row.category_label == CATEGORY_LABELS[complaint.category]
        assert row.status_label == STATUS_LABELS[complaint.status]


def test_rows_are_most_recently_received_first():
    dates = [row.received_date for row in services.list_complaint_rows()]
    assert dates == sorted(dates, reverse=True)
