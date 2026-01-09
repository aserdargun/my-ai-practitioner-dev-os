"""Tests for grading module."""

import pytest

from evals.graders import (
    ContainsGrader,
    ExactMatchGrader,
    KeywordGrader,
    LengthGrader,
    NumericGrader,
)


class TestExactMatchGrader:
    """Tests for ExactMatchGrader."""

    def test_exact_match(self):
        """Test exact match returns full score."""
        grader = ExactMatchGrader()
        result = grader.grade("hello", "hello")
        assert result.score == 1.0
        assert result.passed is True

    def test_no_match(self):
        """Test no match returns zero score."""
        grader = ExactMatchGrader()
        result = grader.grade("hello", "world")
        assert result.score == 0.0
        assert result.passed is False

    def test_case_insensitive(self):
        """Test case insensitive matching."""
        grader = ExactMatchGrader(case_sensitive=False)
        result = grader.grade("Hello", "hello")
        assert result.passed is True

    def test_case_sensitive(self):
        """Test case sensitive matching."""
        grader = ExactMatchGrader(case_sensitive=True)
        result = grader.grade("Hello", "hello")
        assert result.passed is False

    def test_whitespace_handling(self):
        """Test whitespace is trimmed."""
        grader = ExactMatchGrader()
        result = grader.grade("  hello  ", "hello")
        assert result.passed is True


class TestKeywordGrader:
    """Tests for KeywordGrader."""

    def test_all_keywords_present(self):
        """Test all keywords present."""
        grader = KeywordGrader()
        result = grader.grade("hello world", "hello world")
        assert result.score == 1.0
        assert result.passed is True

    def test_partial_keywords(self):
        """Test partial keyword match."""
        grader = KeywordGrader(threshold=0.5)
        result = grader.grade("hello there", "hello world")
        assert result.score == 0.5
        assert result.passed is True

    def test_no_keywords(self):
        """Test no keywords match."""
        grader = KeywordGrader()
        result = grader.grade("goodbye", "hello world")
        assert result.score == 0.0
        assert result.passed is False


class TestContainsGrader:
    """Tests for ContainsGrader."""

    def test_contains(self):
        """Test prediction contains expected."""
        grader = ContainsGrader()
        result = grader.grade("The answer is Paris, France", "Paris")
        assert result.passed is True

    def test_not_contains(self):
        """Test prediction does not contain expected."""
        grader = ContainsGrader()
        result = grader.grade("The answer is London", "Paris")
        assert result.passed is False

    def test_case_insensitive(self):
        """Test case insensitive contains."""
        grader = ContainsGrader(case_sensitive=False)
        result = grader.grade("The answer is PARIS", "paris")
        assert result.passed is True


class TestNumericGrader:
    """Tests for NumericGrader."""

    def test_exact_number(self):
        """Test exact number match."""
        grader = NumericGrader()
        result = grader.grade("The answer is 42", "42")
        assert result.passed is True

    def test_within_tolerance(self):
        """Test number within tolerance."""
        grader = NumericGrader(tolerance=0.1)
        result = grader.grade("10.5", "10")
        assert result.passed is True

    def test_outside_tolerance(self):
        """Test number outside tolerance."""
        grader = NumericGrader(tolerance=0.01)
        result = grader.grade("15", "10")
        assert result.passed is False

    def test_no_number(self):
        """Test no number in text."""
        grader = NumericGrader()
        result = grader.grade("no number here", "42")
        assert result.passed is False


class TestLengthGrader:
    """Tests for LengthGrader."""

    def test_within_range(self):
        """Test length within range."""
        grader = LengthGrader(min_length=5, max_length=20)
        result = grader.grade("hello world", "")
        assert result.passed is True

    def test_too_short(self):
        """Test length too short."""
        grader = LengthGrader(min_length=20, max_length=100)
        result = grader.grade("hi", "")
        assert result.passed is False
        assert "Too short" in result.reason

    def test_too_long(self):
        """Test length too long."""
        grader = LengthGrader(min_length=1, max_length=5)
        result = grader.grade("hello world", "")
        assert result.passed is False
        assert "Too long" in result.reason
