# Evaluation Harness Template

A template for building ML model evaluation frameworks.

## Features

- Multiple grading strategies
- Golden set management
- Metrics calculation
- Report generation
- Test suite included

## Quick Start

```bash
# Install dependencies
pip install -e .

# Run evaluations
python evals/run_evals.py --dataset datasets/sample_golden.jsonl

# Run tests
pytest
```

## Project Structure

```
template-eval-harness/
├── evals/
│   ├── run_evals.py     # Evaluation runner
│   └── graders.py       # Grading strategies
├── datasets/
│   └── sample_golden.jsonl  # Sample test data
├── tests/
│   └── test_graders.py  # Test suite
├── pyproject.toml       # Dependencies and config
└── README.md            # This file
```

## Usage

### Run Evaluations

```python
from evals.run_evals import EvalRunner
from evals.graders import ExactMatchGrader, KeywordGrader

runner = EvalRunner()
runner.add_grader("exact", ExactMatchGrader())
runner.add_grader("keywords", KeywordGrader())

results = runner.run("datasets/sample_golden.jsonl")
runner.print_report(results)
```

### Create Custom Grader

```python
from evals.graders import BaseGrader, GradeResult

class MyGrader(BaseGrader):
    def grade(self, prediction: str, expected: str) -> GradeResult:
        # Your grading logic
        score = calculate_score(prediction, expected)
        return GradeResult(score=score, passed=score > 0.8)
```

### Golden Set Format

```jsonl
{"input": "What is 2+2?", "expected": "4", "metadata": {"category": "math"}}
{"input": "Capital of France?", "expected": "Paris", "metadata": {"category": "geography"}}
```

## Metrics

- **Accuracy**: Percentage of correct predictions
- **Precision/Recall**: For classification tasks
- **F1 Score**: Harmonic mean of precision and recall
- **Mean Score**: Average grader score across examples

## Customization

1. Add custom graders in `graders.py`
2. Create golden sets in `datasets/`
3. Configure thresholds in runner
4. Add custom metrics as needed

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=evals

# Run specific test
pytest tests/test_graders.py -v
```
