# Path Engine

Evaluation and adaptation scripts for the AI Practitioner Booster 2026 learning system.

## Overview

The path engine implements the recommendation loop:

1. **Evaluate** → Compute progress scores
2. **Adapt** → Propose path changes
3. **Report** → Generate tracker updates

All scripts use Python stdlib only—no external dependencies.

## Scripts

| Script | Purpose | Output |
|--------|---------|--------|
| [evaluate.py](evaluate.py) | Compute progress scores | JSON to stdout |
| [adapt.py](adapt.py) | Propose adaptations | JSON to stdout |
| [report.py](report.py) | Generate tracker | Markdown file |

## Usage

```bash
# From repository root
python .claude/path-engine/evaluate.py
python .claude/path-engine/adapt.py
python .claude/path-engine/report.py
```

### With Commands

These scripts are invoked by Claude Code commands:

- `/evaluate` → runs evaluate.py
- `/adapt-path` → runs adapt.py
- `/status` → reads from these outputs

## Human-in-the-Loop

**Critical**: The adaptation flow requires user approval:

```
evaluate.py → scores
     ↓
adapt.py → proposals (NOT auto-applied)
     ↓
User reviews proposals
     ↓
User approves specific changes
     ↓
Changes are applied
```

adapt.py **never** modifies files automatically.

## Scoring Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completion | 30% | Deliverables shipped vs. planned |
| Quality | 25% | DoD criteria met, tests passing |
| Consistency | 20% | Regular progress logging |
| Depth | 15% | Stretch goals attempted |
| Reflection | 10% | Retros and best practices captured |

## Allowed Adaptations

adapt.py can only propose these changes:

| Adaptation | Description |
|------------|-------------|
| Level change | Upgrade/downgrade (Beginner ↔ Intermediate ↔ Advanced) |
| Month reorder | Swap upcoming months within tier scope |
| Remediation week | Insert 1-week remediation block |
| Project swap | Replace project with equivalent scope alternative |

## Data Sources

The engine reads from:

- `.claude/memory/learner_profile.json` — Goals and constraints
- `.claude/memory/progress_log.jsonl` — Progress events
- `.claude/memory/decisions.jsonl` — Past decisions
- `paths/Advanced/tracker.md` — Current progress tracker
- Month README files — DoD criteria

## Output Formats

### evaluate.py

```json
{
  "timestamp": "2026-01-09T10:00:00Z",
  "overall_score": 7.5,
  "dimensions": {
    "completion": 7,
    "quality": 8,
    "consistency": 6,
    "depth": 8,
    "reflection": 9
  },
  "signals": {
    "events_this_week": 5,
    "deliverables_shipped": 2,
    "retros_completed": 1
  },
  "recommendations": [
    "Improve consistency by logging daily"
  ]
}
```

### adapt.py

```json
{
  "timestamp": "2026-01-09T10:00:00Z",
  "evaluation_score": 7.5,
  "proposals": [
    {
      "type": "remediation_week",
      "rationale": "Score dropped below 7.0, recommend consolidation",
      "impact": "Month 4 starts 1 week later",
      "requires_approval": true
    }
  ],
  "no_change_reason": null
}
```

### report.py

Generates `paths/Advanced/tracker.md` with:

- Current position (month, week)
- Progress summary
- Scores history
- Upcoming milestones

## Extending

To modify scoring or adaptation logic:

1. Edit the relevant Python file
2. Maintain JSON output format
3. Update this README
4. Update `docs/evaluation/*.md`

## Testing

```bash
# Dry run evaluation
python .claude/path-engine/evaluate.py --dry-run

# Verbose output
python .claude/path-engine/evaluate.py --verbose
```
