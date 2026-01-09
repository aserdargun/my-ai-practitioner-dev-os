"""Grading Strategies Module."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class GradeResult:
    """Result of grading a single prediction."""

    score: float  # 0.0 to 1.0
    passed: bool
    reason: str = ""


class BaseGrader(ABC):
    """Base class for graders."""

    @abstractmethod
    def grade(self, prediction: str, expected: str) -> GradeResult:
        """Grade a prediction against expected output."""
        pass


class ExactMatchGrader(BaseGrader):
    """Grades based on exact string match."""

    def __init__(self, case_sensitive: bool = False):
        """Initialize grader.

        Args:
            case_sensitive: Whether to do case-sensitive matching
        """
        self.case_sensitive = case_sensitive

    def grade(self, prediction: str, expected: str) -> GradeResult:
        """Grade prediction."""
        if self.case_sensitive:
            match = prediction.strip() == expected.strip()
        else:
            match = prediction.strip().lower() == expected.strip().lower()

        return GradeResult(
            score=1.0 if match else 0.0,
            passed=match,
            reason="Exact match" if match else "No match",
        )


class KeywordGrader(BaseGrader):
    """Grades based on keyword presence."""

    def __init__(self, threshold: float = 0.5):
        """Initialize grader.

        Args:
            threshold: Minimum score to pass
        """
        self.threshold = threshold

    def grade(self, prediction: str, expected: str) -> GradeResult:
        """Grade prediction based on keyword overlap."""
        pred_words = set(prediction.lower().split())
        exp_words = set(expected.lower().split())

        if not exp_words:
            return GradeResult(score=1.0, passed=True, reason="No keywords expected")

        overlap = pred_words & exp_words
        score = len(overlap) / len(exp_words)
        passed = score >= self.threshold

        return GradeResult(
            score=score,
            passed=passed,
            reason=f"Found {len(overlap)}/{len(exp_words)} keywords",
        )


class ContainsGrader(BaseGrader):
    """Grades based on whether prediction contains expected."""

    def __init__(self, case_sensitive: bool = False):
        """Initialize grader."""
        self.case_sensitive = case_sensitive

    def grade(self, prediction: str, expected: str) -> GradeResult:
        """Grade prediction."""
        if self.case_sensitive:
            contains = expected.strip() in prediction
        else:
            contains = expected.strip().lower() in prediction.lower()

        return GradeResult(
            score=1.0 if contains else 0.0,
            passed=contains,
            reason="Contains expected" if contains else "Missing expected",
        )


class NumericGrader(BaseGrader):
    """Grades numeric predictions with tolerance."""

    def __init__(self, tolerance: float = 0.01):
        """Initialize grader.

        Args:
            tolerance: Relative tolerance for matching
        """
        self.tolerance = tolerance

    def _extract_number(self, text: str) -> float | None:
        """Extract first number from text."""
        import re

        match = re.search(r"-?\d+\.?\d*", text)
        if match:
            return float(match.group())
        return None

    def grade(self, prediction: str, expected: str) -> GradeResult:
        """Grade numeric prediction."""
        pred_num = self._extract_number(prediction)
        exp_num = self._extract_number(expected)

        if pred_num is None or exp_num is None:
            return GradeResult(
                score=0.0,
                passed=False,
                reason="Could not extract numbers",
            )

        if exp_num == 0:
            match = pred_num == 0
        else:
            relative_error = abs(pred_num - exp_num) / abs(exp_num)
            match = relative_error <= self.tolerance

        score = 1.0 if match else max(0, 1 - abs(pred_num - exp_num) / (abs(exp_num) + 1))

        return GradeResult(
            score=score,
            passed=match,
            reason=f"Predicted {pred_num}, expected {exp_num}",
        )


class LengthGrader(BaseGrader):
    """Grades based on response length."""

    def __init__(self, min_length: int = 10, max_length: int = 1000):
        """Initialize grader."""
        self.min_length = min_length
        self.max_length = max_length

    def grade(self, prediction: str, expected: str) -> GradeResult:
        """Grade prediction length."""
        length = len(prediction)
        in_range = self.min_length <= length <= self.max_length

        if length < self.min_length:
            reason = f"Too short ({length} < {self.min_length})"
        elif length > self.max_length:
            reason = f"Too long ({length} > {self.max_length})"
        else:
            reason = f"Length OK ({length})"

        return GradeResult(
            score=1.0 if in_range else 0.0,
            passed=in_range,
            reason=reason,
        )
