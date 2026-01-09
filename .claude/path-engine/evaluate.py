#!/usr/bin/env python3
"""
Evaluation Engine for AI Practitioner Booster 2026

Computes progress scores based on memory files and repo signals.
Uses Python stdlib only - no external dependencies.

Usage:
    python evaluate.py [--verbose] [--dry-run]
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


# Paths
REPO_ROOT = Path(__file__).parent.parent.parent
MEMORY_DIR = REPO_ROOT / ".claude" / "memory"
PATHS_DIR = REPO_ROOT / "paths" / "Advanced"

# Scoring weights
WEIGHTS = {
    "completion": 0.30,
    "quality": 0.25,
    "consistency": 0.20,
    "depth": 0.15,
    "reflection": 0.10,
}


def load_json(path: Path) -> Any:
    """Load JSON file."""
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def load_jsonl(path: Path) -> list:
    """Load JSON lines file."""
    if not path.exists():
        return []
    events = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return events


def parse_date(date_str: str) -> datetime:
    """Parse ISO date string."""
    # Handle various formats
    for fmt in ["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return datetime.now()


def get_recent_events(events: list, days: int = 7) -> list:
    """Filter events from the last N days."""
    cutoff = datetime.now() - timedelta(days=days)
    recent = []
    for event in events:
        try:
            event_time = parse_date(event.get("timestamp", ""))
            if event_time >= cutoff:
                recent.append(event)
        except Exception:
            pass
    return recent


def score_completion(events: list, profile: dict) -> tuple[int, dict]:
    """Score based on deliverables completed."""
    # Count deliverable events
    shipped = [e for e in events if e.get("event") == "deliverable_shipped"]
    week_completes = [e for e in events if e.get("event") == "week_complete"]

    # Simple heuristic: expect ~1 deliverable per week
    current_month = profile.get("schedule", {}).get("current_month", 1)
    current_week = profile.get("schedule", {}).get("current_week", 1)
    expected_weeks = (current_month - 1) * 4 + current_week

    # Calculate completion rate
    if expected_weeks == 0:
        score = 10
    else:
        # Count weeks marked complete
        completed_weeks = len([w for w in week_completes if w.get("status") in ["complete", "partial"]])
        rate = min(completed_weeks / max(expected_weeks, 1), 1.0)
        score = int(rate * 10)

    signals = {
        "deliverables_shipped": len(shipped),
        "weeks_completed": len(week_completes),
        "expected_weeks": expected_weeks,
    }

    return score, signals


def score_quality(events: list, profile: dict) -> tuple[int, dict]:
    """Score based on quality indicators."""
    # Look for quality-related events
    reviews = [e for e in events if "review" in e.get("event", "")]
    tests_passing = [e for e in events if "test" in e.get("event", "").lower()]

    # Check for "complete" vs "partial" week completions
    week_completes = [e for e in events if e.get("event") == "week_complete"]
    complete_count = len([w for w in week_completes if w.get("status") == "complete"])
    partial_count = len([w for w in week_completes if w.get("status") == "partial"])

    # Quality score based on completion status
    if week_completes:
        complete_rate = complete_count / len(week_completes)
        score = int(5 + complete_rate * 5)  # 5-10 range
    else:
        score = 7  # Default

    signals = {
        "complete_weeks": complete_count,
        "partial_weeks": partial_count,
        "reviews": len(reviews),
    }

    return score, signals


def score_consistency(events: list, profile: dict) -> tuple[int, dict]:
    """Score based on regular progress logging."""
    # Count unique days with events in the last 14 days
    recent = get_recent_events(events, days=14)

    days_with_events = set()
    for event in recent:
        try:
            event_time = parse_date(event.get("timestamp", ""))
            days_with_events.add(event_time.date())
        except Exception:
            pass

    # Expect logging on most weekdays (10 days in 2 weeks)
    expected_days = 10
    actual_days = len(days_with_events)

    rate = min(actual_days / expected_days, 1.0)
    score = int(rate * 10)

    signals = {
        "days_with_events_14d": actual_days,
        "expected_days": expected_days,
    }

    return score, signals


def score_depth(events: list, profile: dict) -> tuple[int, dict]:
    """Score based on stretch goals and exploration."""
    # Look for depth indicators
    stretch_events = [e for e in events if "stretch" in str(e).lower()]
    research_events = [e for e in events if e.get("event") == "research"]
    extra_learning = [e for e in events if "learning" in str(e).lower()]

    # Count any indication of going beyond basics
    depth_indicators = len(stretch_events) + len(research_events) + len(extra_learning)

    if depth_indicators >= 5:
        score = 10
    elif depth_indicators >= 3:
        score = 8
    elif depth_indicators >= 1:
        score = 6
    else:
        score = 5  # Neutral - not bad, just basics only

    signals = {
        "stretch_events": len(stretch_events),
        "research_events": len(research_events),
    }

    return score, signals


def score_reflection(events: list, profile: dict) -> tuple[int, dict]:
    """Score based on retrospectives and best practices."""
    # Count retro events
    retros = [e for e in events if e.get("event") == "retro_complete" or "retro" in str(e).lower()]

    # Check best practices file
    best_practices_path = MEMORY_DIR / "best_practices.md"
    practice_count = 0
    if best_practices_path.exists():
        content = best_practices_path.read_text()
        # Count dated entries (## YYYY-MM-DD pattern)
        import re
        practice_count = len(re.findall(r"## \d{4}-\d{2}-\d{2}", content))

    # Score based on reflection activity
    reflection_score = min(len(retros) * 2 + practice_count, 10)

    signals = {
        "retros_completed": len(retros),
        "best_practices_added": practice_count,
    }

    return max(reflection_score, 5), signals  # Minimum 5


def compute_overall_score(dimensions: dict[str, int]) -> float:
    """Compute weighted overall score."""
    total = 0.0
    for dim, score in dimensions.items():
        weight = WEIGHTS.get(dim, 0)
        total += score * weight
    return round(total, 2)


def generate_recommendations(dimensions: dict[str, int], overall: float) -> list[str]:
    """Generate improvement recommendations."""
    recommendations = []

    if dimensions.get("consistency", 10) < 7:
        recommendations.append("Improve consistency by logging progress daily, even brief notes.")

    if dimensions.get("reflection", 10) < 7:
        recommendations.append("Run weekly retros (/retro) and capture best practices.")

    if dimensions.get("completion", 10) < 6:
        recommendations.append("Focus on shipping deliverables. Consider reducing scope with /ship-mvp.")

    if dimensions.get("depth", 10) < 6:
        recommendations.append("Try at least one stretch goal this month to deepen learning.")

    if overall < 6.0:
        recommendations.append("Consider a remediation week to consolidate before moving on.")

    if not recommendations:
        recommendations.append("Great progress! Keep up the momentum.")

    return recommendations


def evaluate(verbose: bool = False) -> dict:
    """Run full evaluation."""
    # Load data
    profile = load_json(MEMORY_DIR / "learner_profile.json") or {}
    progress_log = load_jsonl(MEMORY_DIR / "progress_log.jsonl")
    decisions = load_jsonl(MEMORY_DIR / "decisions.jsonl")

    # Combine all events for analysis
    all_events = progress_log + decisions

    if verbose:
        print(f"Loaded {len(progress_log)} progress events", file=sys.stderr)
        print(f"Loaded {len(decisions)} decisions", file=sys.stderr)

    # Score each dimension
    dimensions = {}
    all_signals = {}

    completion_score, completion_signals = score_completion(all_events, profile)
    dimensions["completion"] = completion_score
    all_signals.update(completion_signals)

    quality_score, quality_signals = score_quality(all_events, profile)
    dimensions["quality"] = quality_score
    all_signals.update(quality_signals)

    consistency_score, consistency_signals = score_consistency(all_events, profile)
    dimensions["consistency"] = consistency_score
    all_signals.update(consistency_signals)

    depth_score, depth_signals = score_depth(all_events, profile)
    dimensions["depth"] = depth_score
    all_signals.update(depth_signals)

    reflection_score, reflection_signals = score_reflection(all_events, profile)
    dimensions["reflection"] = reflection_score
    all_signals.update(reflection_signals)

    # Compute overall
    overall_score = compute_overall_score(dimensions)

    # Generate recommendations
    recommendations = generate_recommendations(dimensions, overall_score)

    # Build result
    result = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "overall_score": overall_score,
        "dimensions": dimensions,
        "signals": all_signals,
        "recommendations": recommendations,
        "learner_level": profile.get("level", "Unknown"),
        "current_month": profile.get("schedule", {}).get("current_month", 1),
        "current_week": profile.get("schedule", {}).get("current_week", 1),
    }

    return result


def main():
    parser = argparse.ArgumentParser(description="Evaluate learning progress")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--dry-run", action="store_true", help="Don't save results")
    args = parser.parse_args()

    result = evaluate(verbose=args.verbose)

    # Output JSON to stdout
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
