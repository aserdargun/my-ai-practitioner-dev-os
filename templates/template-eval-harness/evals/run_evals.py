"""Evaluation Runner Module."""

import json
from dataclasses import dataclass, field
from pathlib import Path

from evals.graders import BaseGrader, ExactMatchGrader, GradeResult, KeywordGrader


@dataclass
class EvalExample:
    """A single evaluation example."""

    input: str
    expected: str
    metadata: dict = field(default_factory=dict)


@dataclass
class EvalResult:
    """Result of evaluating a single example."""

    example: EvalExample
    prediction: str
    grades: dict[str, GradeResult]


@dataclass
class EvalReport:
    """Overall evaluation report."""

    total: int
    passed: int
    failed: int
    accuracy: float
    results: list[EvalResult]
    grader_scores: dict[str, float]


class MockPredictor:
    """Mock predictor for demonstration.

    Replace with your actual model inference.
    """

    def predict(self, input_text: str) -> str:
        """Generate mock prediction."""
        # Simple mock: return the input
        return input_text.lower()


class EvalRunner:
    """Runs evaluations on a dataset."""

    def __init__(self, predictor: MockPredictor | None = None):
        """Initialize runner."""
        self.predictor = predictor or MockPredictor()
        self.graders: dict[str, BaseGrader] = {}

    def add_grader(self, name: str, grader: BaseGrader) -> None:
        """Add a grader to the evaluation."""
        self.graders[name] = grader

    def load_dataset(self, path: str) -> list[EvalExample]:
        """Load evaluation dataset from JSONL file."""
        examples = []
        with open(path, encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                examples.append(
                    EvalExample(
                        input=data["input"],
                        expected=data["expected"],
                        metadata=data.get("metadata", {}),
                    )
                )
        return examples

    def evaluate_example(self, example: EvalExample) -> EvalResult:
        """Evaluate a single example."""
        prediction = self.predictor.predict(example.input)

        grades = {}
        for name, grader in self.graders.items():
            grades[name] = grader.grade(prediction, example.expected)

        return EvalResult(
            example=example,
            prediction=prediction,
            grades=grades,
        )

    def run(self, dataset_path: str) -> EvalReport:
        """Run evaluation on dataset."""
        examples = self.load_dataset(dataset_path)
        results = []

        for example in examples:
            result = self.evaluate_example(example)
            results.append(result)

        # Calculate metrics
        passed = sum(
            1
            for r in results
            if all(g.passed for g in r.grades.values())
        )
        failed = len(results) - passed
        accuracy = passed / len(results) if results else 0.0

        # Calculate per-grader scores
        grader_scores = {}
        for grader_name in self.graders:
            scores = [r.grades[grader_name].score for r in results]
            grader_scores[grader_name] = sum(scores) / len(scores) if scores else 0.0

        return EvalReport(
            total=len(results),
            passed=passed,
            failed=failed,
            accuracy=accuracy,
            results=results,
            grader_scores=grader_scores,
        )

    def print_report(self, report: EvalReport) -> None:
        """Print evaluation report."""
        print("=" * 50)
        print("EVALUATION REPORT")
        print("=" * 50)
        print(f"Total examples: {report.total}")
        print(f"Passed: {report.passed}")
        print(f"Failed: {report.failed}")
        print(f"Accuracy: {report.accuracy:.2%}")
        print()
        print("Grader Scores:")
        for name, score in report.grader_scores.items():
            print(f"  {name}: {score:.3f}")
        print("=" * 50)

        # Show failed examples
        failed = [r for r in report.results if not all(g.passed for g in r.grades.values())]
        if failed:
            print("\nFailed Examples:")
            for i, result in enumerate(failed[:5], 1):
                print(f"\n{i}. Input: {result.example.input[:50]}...")
                print(f"   Expected: {result.example.expected[:50]}...")
                print(f"   Got: {result.prediction[:50]}...")


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Run evaluations")
    parser.add_argument(
        "--dataset",
        default="datasets/sample_golden.jsonl",
        help="Path to dataset",
    )
    args = parser.parse_args()

    runner = EvalRunner()
    runner.add_grader("exact", ExactMatchGrader())
    runner.add_grader("keywords", KeywordGrader())

    report = runner.run(args.dataset)
    runner.print_report(report)


if __name__ == "__main__":
    main()
