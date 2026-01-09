#!/usr/bin/env python3
"""
Adaptation Engine for AI Practitioner Booster 2026

Proposes path changes based on evaluation results.
IMPORTANT: Proposals require explicit user approval before being applied.
Uses Python stdlib only - no external dependencies.

Usage:
    python adapt.py [--verbose] [--score <score>]
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


# Paths
REPO_ROOT = Path(__file__).parent.parent.parent
MEMORY_DIR = REPO_ROOT / ".claude" / "memory"

# Thresholds
LEVEL_DOWN_THRESHOLD = 5.0  # Score below this suggests level downgrade
LEVEL_UP_THRESHOLD = 9.0    # Score above this suggests level upgrade
REMEDIATION_THRESHOLD = 6.5  # Score below this suggests remediation week
ACCELERATION_THRESHOLD = 9.5  # Score above this suggests acceleration

# Allowed adaptation types
ADAPTATION_TYPES = [
    "level_change",
    "month_reorder",
    "remediation_week",
    "project_swap",
]


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


def get_evaluation_score() -> Optional[dict]:
    """Get the latest evaluation score by running evaluate.py."""
    try:
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "evaluate.py")],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception:
        pass
    return None


def check_level_change(score: float, profile: dict) -> Optional[dict]:
    """Check if level change should be proposed."""
    current_level = profile.get("level", "Advanced")
    current_month = profile.get("schedule", {}).get("current_month", 1)

    # Only consider level changes at month boundaries
    current_week = profile.get("schedule", {}).get("current_week", 1)
    if current_week not in [4, 1]:  # End of month or start of new month
        return None

    levels = ["Beginner", "Intermediate", "Advanced"]
    current_idx = levels.index(current_level) if current_level in levels else 2

    # Check for downgrade
    if score < LEVEL_DOWN_THRESHOLD and current_idx > 0:
        new_level = levels[current_idx - 1]
        return {
            "type": "level_change",
            "action": "downgrade",
            "from": current_level,
            "to": new_level,
            "rationale": f"Score {score:.1f} is below {LEVEL_DOWN_THRESHOLD}. "
                        f"Downgrading to {new_level} allows more time to build fundamentals.",
            "impact": f"Curriculum scope reduces. Focus on Tier 1{' + Tier 2' if new_level == 'Intermediate' else ''} only.",
            "requires_approval": True
        }

    # Check for upgrade
    if score >= LEVEL_UP_THRESHOLD and current_idx < 2:
        new_level = levels[current_idx + 1]
        return {
            "type": "level_change",
            "action": "upgrade",
            "from": current_level,
            "to": new_level,
            "rationale": f"Score {score:.1f} is above {LEVEL_UP_THRESHOLD}. "
                        f"Upgrading to {new_level} adds more challenging material.",
            "impact": f"Curriculum scope expands to include Tier {current_idx + 2} content.",
            "requires_approval": True
        }

    return None


def check_remediation_week(score: float, profile: dict, dimensions: dict) -> Optional[dict]:
    """Check if remediation week should be proposed."""
    if score >= REMEDIATION_THRESHOLD:
        return None

    # Identify weakest dimension
    weakest = min(dimensions.items(), key=lambda x: x[1])
    weakest_dim, weakest_score = weakest

    current_month = profile.get("schedule", {}).get("current_month", 1)

    return {
        "type": "remediation_week",
        "duration": "1 week",
        "focus": weakest_dim,
        "rationale": f"Score {score:.1f} is below {REMEDIATION_THRESHOLD}. "
                    f"Weakest area is {weakest_dim} ({weakest_score}/10). "
                    f"Recommend consolidation before moving on.",
        "impact": f"Month {current_month + 1} starts 1 week later. "
                 f"Use the week to strengthen {weakest_dim}.",
        "requires_approval": True
    }


def check_month_reorder(score: float, profile: dict, decisions: list) -> Optional[dict]:
    """Check if month reordering might help."""
    # This is a more complex decision that would need
    # analysis of upcoming months and current struggles
    # For now, we only suggest this in specific cases

    current_month = profile.get("schedule", {}).get("current_month", 1)

    # Only consider after month 3 and before month 10
    if current_month < 3 or current_month > 10:
        return None

    # Check if there's been a recent project swap or remediation
    recent_adaptations = [
        d for d in decisions
        if d.get("decision") in ["project_swap", "remediation_week"]
    ]

    # If already adapted recently, don't suggest more changes
    if len(recent_adaptations) >= 2:
        return None

    # Could add more sophisticated logic here
    return None


def check_project_swap(score: float, profile: dict, dimensions: dict) -> Optional[dict]:
    """Check if project swap might help."""
    # Project swaps are suggested when:
    # 1. Completion is low despite good effort
    # 2. The current project may not align with goals

    if dimensions.get("completion", 10) > 5:
        return None  # Completion is okay

    if dimensions.get("consistency", 10) < 5:
        return None  # Problem might be effort, not project

    current_month = profile.get("schedule", {}).get("current_month", 1)

    return {
        "type": "project_swap",
        "current_month": current_month,
        "rationale": "Completion is low despite consistent effort. "
                    "The current project may be misaligned with your goals or too complex.",
        "impact": "Replace the current month's project with an alternative of equivalent scope. "
                 "Same learning goals, different deliverables.",
        "note": "You'll need to specify an alternative project when approving.",
        "requires_approval": True
    }


def generate_proposals(evaluation: dict, profile: dict, decisions: list) -> list[dict]:
    """Generate all applicable adaptation proposals."""
    proposals = []

    score = evaluation.get("overall_score", 7.0)
    dimensions = evaluation.get("dimensions", {})

    # Check each adaptation type
    level_proposal = check_level_change(score, profile)
    if level_proposal:
        proposals.append(level_proposal)

    remediation_proposal = check_remediation_week(score, profile, dimensions)
    if remediation_proposal:
        proposals.append(remediation_proposal)

    reorder_proposal = check_month_reorder(score, profile, decisions)
    if reorder_proposal:
        proposals.append(reorder_proposal)

    swap_proposal = check_project_swap(score, profile, dimensions)
    if swap_proposal:
        proposals.append(swap_proposal)

    return proposals


def adapt(evaluation: Optional[dict] = None, verbose: bool = False) -> dict:
    """Generate adaptation proposals."""
    # Get evaluation if not provided
    if evaluation is None:
        evaluation = get_evaluation_score()
        if evaluation is None:
            return {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "error": "Could not get evaluation score",
                "proposals": []
            }

    # Load profile and decisions
    profile = load_json(MEMORY_DIR / "learner_profile.json") or {}
    decisions = load_jsonl(MEMORY_DIR / "decisions.jsonl")

    if verbose:
        print(f"Evaluation score: {evaluation.get('overall_score', 'N/A')}", file=sys.stderr)
        print(f"Current level: {profile.get('level', 'Unknown')}", file=sys.stderr)

    # Generate proposals
    proposals = generate_proposals(evaluation, profile, decisions)

    # Determine if no changes needed
    no_change_reason = None
    if not proposals:
        score = evaluation.get("overall_score", 7.0)
        if score >= REMEDIATION_THRESHOLD:
            no_change_reason = f"Score {score:.1f} is healthy. No adaptations needed."
        else:
            no_change_reason = "No applicable adaptations identified."

    # Build result
    result = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "evaluation_score": evaluation.get("overall_score"),
        "evaluation_dimensions": evaluation.get("dimensions"),
        "proposals": proposals,
        "no_change_reason": no_change_reason,
        "note": "All proposals require explicit user approval before being applied."
    }

    return result


def main():
    parser = argparse.ArgumentParser(description="Generate adaptation proposals")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--score", type=float, help="Override evaluation score")
    args = parser.parse_args()

    # Allow score override for testing
    evaluation = None
    if args.score is not None:
        evaluation = {
            "overall_score": args.score,
            "dimensions": {
                "completion": 7,
                "quality": 7,
                "consistency": 7,
                "depth": 7,
                "reflection": 7
            }
        }

    result = adapt(evaluation=evaluation, verbose=args.verbose)

    # Output JSON to stdout
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
