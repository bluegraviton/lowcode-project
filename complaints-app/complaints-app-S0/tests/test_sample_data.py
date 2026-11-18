"""Cross-cutting checks that the sample data is synthetic and consistent."""

import dataclasses
import re
from datetime import date

from app import config
from app.features.complaints.repository import Complaint
from app.sample_data import COMPLAINTS, USERS

REFERENCE_PATTERN = re.compile(r"^CMP-\d{4}-\d{4}$")
FINISHED_STATUSES = (
    config.STATUS_PENDING_APPROVAL,
    config.STATUS_APPROVED,
    config.STATUS_CLOSED,
)


def test_users_match_the_planned_set():
    roles = [user["role"] for user in USERS]
    assert len(USERS) == 3
    assert roles.count(config.ROLE_HANDLER) == 2
    assert roles.count(config.ROLE_COMPLIANCE) == 1


def test_users_are_synthetic_and_valid():
    assert len({user["id"] for user in USERS}) == len(USERS)
    assert len({user["email"] for user in USERS}) == len(USERS)
    for user in USERS:
        assert user["email"].endswith("@example.com")
        assert user["role"] in config.ROLES
        assert user["password_hash"] is None


def test_there_are_eight_complaints():
    assert len(COMPLAINTS) == 8


def test_ids_and_references_are_unique():
    assert len({c["id"] for c in COMPLAINTS}) == len(COMPLAINTS)
    assert len({c["reference"] for c in COMPLAINTS}) == len(COMPLAINTS)
    for c in COMPLAINTS:
        assert REFERENCE_PATTERN.match(c["reference"])


def test_complaint_fields_match_the_record_class():
    expected = {field.name for field in dataclasses.fields(Complaint)}
    for c in COMPLAINTS:
        assert set(c) == expected


def test_complaints_are_synthetic():
    for c in COMPLAINTS:
        assert c["complainant_email"].endswith("@example.com")
        assert c["complainant_phone"] is None


def test_enumeration_values_are_valid():
    handler_ids = {u["id"] for u in USERS if u["role"] == config.ROLE_HANDLER}
    for c in COMPLAINTS:
        assert c["handler_id"] in handler_ids
        assert c["status"] in config.STATUSES
        assert c["received_channel"] in config.CHANNELS
        assert c["product"] in config.PRODUCTS
        assert c["category"] in config.CATEGORIES
        assert c["outcome"] in (*config.OUTCOMES, None)
        assert c["root_cause_category"] in (*config.ROOT_CAUSES, None)
        assert c["day40_outcome"] in (*config.DAY40_OUTCOMES, None)
        assert c["redress_amount"] >= 0


def test_all_five_states_are_present():
    assert {c["status"] for c in COMPLAINTS} == set(config.STATUSES)


def test_fields_are_consistent_with_status():
    for c in COMPLAINTS:
        finished = c["status"] in FINISHED_STATUSES
        assert (c["outcome"] is not None) == finished
        assert (c["completed_at"] is not None) == finished
        closed = c["status"] == config.STATUS_CLOSED
        assert (c["closed_at"] is not None) == closed
        assert (c["day40_outcome"] is not None) == closed


def test_timestamps_are_utc_aware_and_ordered():
    for c in COMPLAINTS:
        assert c["created_at"].tzinfo is not None
        assert c["created_at"].date() >= c["received_date"]
        assert c["updated_at"] >= c["created_at"]


def test_an_old_and_a_near_day_40_investigation_are_included():
    # About 8 weeks before 11 November 2026 is 16 September 2026.
    old_open = [
        c
        for c in COMPLAINTS
        if c["status"] == config.STATUS_INVESTIGATING
        and c["received_date"] <= date(2026, 9, 16)
    ]
    assert len(old_open) >= 2
