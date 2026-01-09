"""Data Pipeline - Main Execution Module."""

import argparse
import csv
import logging
from dataclasses import dataclass
from pathlib import Path

from pipeline.validate import DataValidator, ValidationResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    """Result of pipeline execution."""

    success: bool
    records_processed: int
    records_valid: int
    records_invalid: int
    errors: list[str]


class Pipeline:
    """Data processing pipeline."""

    def __init__(self, schema: dict | None = None):
        """Initialize pipeline with optional schema."""
        self.schema = schema or {
            "id": {"type": "int", "required": True},
            "name": {"type": "str", "required": True},
            "value": {"type": "float", "required": False},
        }
        self.validator = DataValidator(self.schema)

    def load_csv(self, path: Path) -> list[dict]:
        """Load data from CSV file."""
        records = []
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
        return records

    def save_csv(self, records: list[dict], path: Path) -> None:
        """Save data to CSV file."""
        if not records:
            return

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)

    def transform(self, record: dict) -> dict:
        """Apply transformations to a record."""
        # Convert types based on schema
        transformed = {}
        for key, value in record.items():
            if key in self.schema:
                field_type = self.schema[key].get("type", "str")
                if field_type == "int" and value:
                    transformed[key] = int(value)
                elif field_type == "float" and value:
                    transformed[key] = float(value)
                else:
                    transformed[key] = value
            else:
                transformed[key] = value
        return transformed

    def run(self, input_path: str, output_path: str) -> PipelineResult:
        """Execute the pipeline."""
        logger.info(f"Starting pipeline: {input_path} -> {output_path}")
        errors = []
        valid_records = []
        invalid_count = 0

        try:
            # Load data
            records = self.load_csv(Path(input_path))
            logger.info(f"Loaded {len(records)} records")

            # Process each record
            for i, record in enumerate(records):
                # Validate
                result = self.validator.validate_record(record)
                if not result.is_valid:
                    invalid_count += 1
                    errors.extend([f"Record {i}: {e}" for e in result.errors])
                    continue

                # Transform
                try:
                    transformed = self.transform(record)
                    valid_records.append(transformed)
                except Exception as e:
                    invalid_count += 1
                    errors.append(f"Record {i}: Transform error - {e}")

            # Save valid records
            self.save_csv(valid_records, Path(output_path))
            logger.info(f"Saved {len(valid_records)} valid records")

            return PipelineResult(
                success=True,
                records_processed=len(records),
                records_valid=len(valid_records),
                records_invalid=invalid_count,
                errors=errors,
            )

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            return PipelineResult(
                success=False,
                records_processed=0,
                records_valid=0,
                records_invalid=0,
                errors=[str(e)],
            )


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Run data pipeline")
    parser.add_argument("--input", required=True, help="Input CSV file")
    parser.add_argument("--output", required=True, help="Output CSV file")
    args = parser.parse_args()

    pipeline = Pipeline()
    result = pipeline.run(args.input, args.output)

    print(f"Success: {result.success}")
    print(f"Processed: {result.records_processed}")
    print(f"Valid: {result.records_valid}")
    print(f"Invalid: {result.records_invalid}")

    if result.errors:
        print("Errors:")
        for error in result.errors[:10]:  # Show first 10 errors
            print(f"  - {error}")


if __name__ == "__main__":
    main()
