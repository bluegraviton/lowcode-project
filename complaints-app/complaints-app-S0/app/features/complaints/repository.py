"""Complaints repository: the only place this feature touches the data store.

In S0 the store is app.sample_data. In S1 and S2b only this file is rewritten
to read from SQLite; the function names, arguments and returned field names
stay the same, so services and templates do not change.
"""

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from app import sample_data


@dataclass(frozen=True)
class Complaint:
    """One complaint record. Field names follow Core Spec Section 7."""

    id: int
    reference: str
    handler_id: int
    complainant_name: str
    complainant_email: str
    complainant_phone: Optional[str]
    received_date: date
    received_channel: str
    receipt_note: Optional[str]
    product: str
    category: str
    description: str
    status: str
    findings: Optional[str]
    root_cause_category: Optional[str]
    outcome: Optional[str]
    outcome_rationale: Optional[str]
    redress_amount: Decimal
    revision: int
    completed_at: Optional[datetime]
    day40_outcome: Optional[str]
    closed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


def list_complaints() -> list[Complaint]:
    """Return every complaint as an immutable record built from a copy."""
    return [Complaint(**dict(row)) for row in sample_data.COMPLAINTS]
