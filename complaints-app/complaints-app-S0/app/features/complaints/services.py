"""Complaints service: turns repository records into what the page shows."""

from dataclasses import dataclass
from datetime import date

from app.config import CATEGORY_LABELS, PRODUCT_LABELS, STATUS_LABELS
from app.features.complaints import repository


@dataclass(frozen=True)
class ComplaintRow:
    """One row of the complaints list, with display text already resolved."""

    reference: str
    complainant_name: str
    product_label: str
    category_label: str
    status_label: str
    received_date: date


def list_complaint_rows() -> list[ComplaintRow]:
    """Return list rows, most recently received first."""
    complaints = sorted(
        repository.list_complaints(),
        key=lambda c: (c.received_date, c.reference),
        reverse=True,
    )
    return [
        ComplaintRow(
            reference=c.reference,
            complainant_name=c.complainant_name,
            product_label=PRODUCT_LABELS[c.product],
            category_label=CATEGORY_LABELS[c.category],
            status_label=STATUS_LABELS[c.status],
            received_date=c.received_date,
        )
        for c in complaints
    ]
