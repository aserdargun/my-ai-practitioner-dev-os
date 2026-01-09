"""Data Validation Module."""

from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Result of validation."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)


class DataValidator:
    """Validates data against a schema."""

    def __init__(self, schema: dict):
        """Initialize with schema definition.

        Schema format:
        {
            "field_name": {
                "type": "int" | "float" | "str" | "bool",
                "required": True | False,
                "min": <number>,  # optional, for numeric types
                "max": <number>,  # optional, for numeric types
            }
        }
        """
        self.schema = schema

    def validate_record(self, record: dict) -> ValidationResult:
        """Validate a single record against the schema."""
        errors = []

        # Check required fields
        for field_name, field_spec in self.schema.items():
            if field_spec.get("required", False):
                if field_name not in record or record[field_name] in (None, ""):
                    errors.append(f"Missing required field: {field_name}")

        # Validate field types and constraints
        for field_name, value in record.items():
            if field_name not in self.schema:
                continue  # Skip unknown fields

            if value in (None, ""):
                continue  # Skip empty optional fields

            field_spec = self.schema[field_name]
            field_type = field_spec.get("type", "str")

            # Type validation
            try:
                if field_type == "int":
                    int_val = int(value)
                    if "min" in field_spec and int_val < field_spec["min"]:
                        errors.append(
                            f"{field_name}: value {int_val} below min {field_spec['min']}"
                        )
                    if "max" in field_spec and int_val > field_spec["max"]:
                        errors.append(
                            f"{field_name}: value {int_val} above max {field_spec['max']}"
                        )
                elif field_type == "float":
                    float_val = float(value)
                    if "min" in field_spec and float_val < field_spec["min"]:
                        errors.append(
                            f"{field_name}: value {float_val} below min {field_spec['min']}"
                        )
                    if "max" in field_spec and float_val > field_spec["max"]:
                        errors.append(
                            f"{field_name}: value {float_val} above max {field_spec['max']}"
                        )
                elif field_type == "bool":
                    if str(value).lower() not in ("true", "false", "0", "1"):
                        errors.append(f"{field_name}: invalid boolean value '{value}'")
            except (ValueError, TypeError):
                errors.append(f"{field_name}: cannot convert '{value}' to {field_type}")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
        )

    def validate(self, records: list[dict]) -> ValidationResult:
        """Validate multiple records."""
        all_errors = []
        for i, record in enumerate(records):
            result = self.validate_record(record)
            if not result.is_valid:
                all_errors.extend([f"Record {i}: {e}" for e in result.errors])

        return ValidationResult(
            is_valid=len(all_errors) == 0,
            errors=all_errors,
        )
