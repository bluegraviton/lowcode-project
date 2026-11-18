"""Tests for the complaints repository."""

import dataclasses

import pytest

from app.features.complaints import repository


def test_records_are_frozen_dataclasses():
    record = repository.list_complaints()[0]
    assert dataclasses.is_dataclass(record)
    with pytest.raises(dataclasses.FrozenInstanceError):
        record.status = "changed"


def test_records_use_attribute_access():
    record = repository.list_complaints()[0]
    assert record.reference.startswith("CMP-")
    assert record.received_date is not None


def test_each_call_returns_a_fresh_list():
    first = repository.list_complaints()
    first.clear()
    assert len(repository.list_complaints()) > 0
