# Tests

Unit tests for the mini-example sentiment classifier.

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src

# Run specific test
pytest tests/test_model.py::test_predict_positive -v
```

## Test Structure

| Test | Purpose |
|------|---------|
| `test_tokenize` | Verify tokenization works correctly |
| `test_train` | Verify training improves model |
| `test_predict_positive` | Verify positive sentiment detection |
| `test_predict_negative` | Verify negative sentiment detection |
| `test_save_load` | Verify model serialization |

## Writing More Tests

When adding tests:

1. Test edge cases (empty input, very long input)
2. Test error handling
3. Test with diverse examples
4. Check confidence scores are reasonable
