"""Tests for data validation module."""

import pytest

from pipeline.validate import DataValidator, ValidationResult


@pytest.fixture
def validator():
    """Create validator with test schema."""
    schema = {
        "id": {"type": "int", "required": True, "min": 1},
        "name": {"type": "str", "required": True},
        "value": {"type": "float", "required": False, "min": 0.0, "max": 100.0},
        "active": {"type": "bool", "required": False},
    }
    return DataValidator(schema)


def test_valid_record(validator):
    """Test validation of valid record."""
    record = {"id": "1", "name": "test", "value": "50.0", "active": "true"}
    result = validator.validate_record(record)
    assert result.is_valid
    assert len(result.errors) == 0


def test_missing_required_field(validator):
    """Test validation fails for missing required field."""
    record = {"id": "1"}  # Missing 'name'
    result = validator.validate_record(record)
    assert not result.is_valid
    assert any("Missing required field: name" in e for e in result.errors)


def test_invalid_type(validator):
    """Test validation fails for invalid type."""
    record = {"id": "not_an_int", "name": "test"}
    result = validator.validate_record(record)
    assert not result.is_valid
    assert any("cannot convert" in e for e in result.errors)


def test_value_below_min(validator):
    """Test validation fails for value below minimum."""
    record = {"id": "0", "name": "test"}  # id min is 1
    result = validator.validate_record(record)
    assert not result.is_valid
    assert any("below min" in e for e in result.errors)


def test_value_above_max(validator):
    """Test validation fails for value above maximum."""
    record = {"id": "1", "name": "test", "value": "150.0"}  # value max is 100
    result = validator.validate_record(record)
    assert not result.is_valid
    assert any("above max" in e for e in result.errors)


def test_optional_field_empty(validator):
    """Test optional field can be empty."""
    record = {"id": "1", "name": "test", "value": ""}
    result = validator.validate_record(record)
    assert result.is_valid


def test_validate_multiple_records(validator):
    """Test validation of multiple records."""
    records = [
        {"id": "1", "name": "test1"},
        {"id": "2", "name": "test2"},
        {"id": "invalid", "name": "test3"},
    ]
    result = validator.validate(records)
    assert not result.is_valid
    assert len(result.errors) == 1  # Only record 2 (index) has error


def test_unknown_field_ignored(validator):
    """Test unknown fields are ignored."""
    record = {"id": "1", "name": "test", "unknown_field": "value"}
    result = validator.validate_record(record)
    assert result.is_valid


def test_invalid_boolean(validator):
    """Test invalid boolean value."""
    record = {"id": "1", "name": "test", "active": "maybe"}
    result = validator.validate_record(record)
    assert not result.is_valid
    assert any("invalid boolean" in e for e in result.errors)
