# Evaluation Signals

Data sources used to compute progress scores.

---

## Overview

The evaluation engine reads signals from:

1. Memory files (`.claude/memory/*`)
2. Repository state (files, tests, docs)
3. Tracker state (`paths/Advanced/tracker.md`)
4. Month README files (DoD criteria)

---

## Memory Signals

### From progress_log.jsonl

| Signal | Description | Used For |
|--------|-------------|----------|
| `week_start` count | Weeks initiated | Consistency |
| `week_complete` count | Weeks finished | Completion |
| `week_complete.status` | Complete vs. partial | Quality |
| `deliverable_shipped` count | Milestones hit | Completion |
| `blocker_identified` count | Blocks encountered | Context |
| `blocker_resolved` count | Blocks overcome | Growth |
| Days with events | Unique dates logged | Consistency |
| Events in last 7 days | Recent activity | Consistency |
| Events in last 14 days | Activity trend | Consistency |

### From learner_profile.json

| Signal | Description | Used For |
|--------|-------------|----------|
| `current_month` | Month number | Context |
| `current_week` | Week number | Context |
| `hours_per_week` | Available time | Expectations |

### From decisions.jsonl

| Signal | Description | Used For |
|--------|-------------|----------|
| Decision count | Total decisions made | Engagement |
| Recent adaptations | Path changes made | Context |

### From best_practices.md

| Signal | Description | Used For |
|--------|-------------|----------|
| Entry count | Best practices captured | Reflection |
| Recent entries | Practices in last 30 days | Reflection |

---

## Repository Signals

### Code Metrics

| Signal | Description | Used For |
|--------|-------------|----------|
| Test files exist | Tests written | Quality |
| Test pass rate | Tests passing | Quality |
| Lint status | Ruff/linter clean | Quality |

### Documentation

| Signal | Description | Used For |
|--------|-------------|----------|
| README updated | Recent changes | Quality |
| API docs exist | Documentation written | Quality |

### Git History

| Signal | Description | Used For |
|--------|-------------|----------|
| Commits this week | Activity level | Consistency |
| Commits this month | Monthly activity | Completion |

---

## Tracker Signals

| Signal | Description | Used For |
|--------|-------------|----------|
| Month progress % | Overall progress | Completion |
| Checklist items done | Tasks completed | Completion |

---

## Month README Signals

Each month's README contains:

| Signal | Description | Used For |
|--------|-------------|----------|
| Learning goals | Expected outcomes | Completion |
| Deliverables list | What to ship | Completion |
| DoD checklist | Quality criteria | Quality |
| Stretch goals | Optional extras | Depth |

---

## Signal Collection

### Automatic

The evaluation engine reads files directly:

```python
# Read progress log
with open('.claude/memory/progress_log.jsonl') as f:
    events = [json.loads(line) for line in f if line.strip()]

# Count completions
completions = [e for e in events if e.get('event') == 'week_complete']
```

### On-Demand

Some signals are computed when evaluation runs:

```python
# Check test status
result = subprocess.run(['pytest', '--tb=no', '-q'], capture_output=True)
tests_passing = result.returncode == 0
```

---

## Signal Weighting

Signals contribute to dimensions with varying importance:

### Completion Signals

- Deliverables shipped: High weight
- Week completions: Medium weight
- Month milestones: High weight

### Quality Signals

- Complete (vs. partial) weeks: High weight
- Test status: Medium weight
- DoD checklist: High weight

### Consistency Signals

- Days with events: High weight
- Recent activity (7 days): High weight
- Gaps in activity: Negative weight

### Depth Signals

- Stretch events: High weight
- Research documented: Medium weight
- Extra learning: Medium weight

### Reflection Signals

- Retros completed: High weight
- Best practices added: Medium weight
- Journal entries: Medium weight

---

## Adding New Signals

To add a new signal:

1. Identify the data source
2. Add reading logic to `evaluate.py`
3. Integrate into dimension scoring
4. Update this documentation

Example:

```python
# New signal: track code review feedback
reviews = [e for e in events if 'review' in e.get('event', '')]
signals['reviews_received'] = len(reviews)
```

---

## Debugging Signals

### View Raw Data

```bash
# Progress log
cat .claude/memory/progress_log.jsonl | jq .

# Best practices count
grep -c "^## " .claude/memory/best_practices.md
```

### Run Verbose Evaluation

```bash
python .claude/path-engine/evaluate.py --verbose
```

This shows which signals were read and how they contributed.

---

## Links

- [Evaluation rubric](rubric.md)
- [Scoring details](scoring.md)
- [Path engine](../../.claude/path-engine/)
