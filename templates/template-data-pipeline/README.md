# Data Pipeline Template

A template for building data validation and processing pipelines.

## Features

- Data validation with schema checks
- Pipeline execution with error handling
- Quality reports
- Test suite included

## Quick Start

```bash
# Install dependencies
pip install -e .

# Run the pipeline
python pipeline/run.py --input data.csv --output processed.csv

# Run tests
pytest
```

## Project Structure

```
template-data-pipeline/
├── pipeline/
│   ├── run.py           # Pipeline execution
│   └── validate.py      # Data validation
├── tests/
│   └── test_validate.py # Test suite
├── pyproject.toml       # Dependencies and config
└── README.md            # This file
```

## Usage

### Validate Data

```python
from pipeline.validate import DataValidator

validator = DataValidator(schema={
    "id": {"type": "int", "required": True},
    "name": {"type": "str", "required": True},
    "value": {"type": "float", "required": False},
})

result = validator.validate(data)
print(f"Valid: {result.is_valid}")
print(f"Errors: {result.errors}")
```

### Run Pipeline

```python
from pipeline.run import Pipeline

pipeline = Pipeline()
result = pipeline.run(
    input_path="data.csv",
    output_path="processed.csv",
)
```

## Customization

1. Add your schema definitions to `validate.py`
2. Extend the `Pipeline` class with custom steps
3. Add transformations as needed
4. Configure logging for production

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pipeline

# Run specific test
pytest tests/test_validate.py -v
```
