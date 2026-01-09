# Memory System Guide

How the learning state is stored and managed.

---

## Overview

The memory system stores your learning journey:

| File | Purpose | Format |
|------|---------|--------|
| `learner_profile.json` | Goals, constraints, schedule | JSON |
| `progress_log.jsonl` | Timestamped events | JSON Lines |
| `decisions.jsonl` | Important decisions | JSON Lines |
| `best_practices.md` | Learnings captured | Markdown |

All files are in `.claude/memory/`.

---

## Key Principles

### Append-Only

Memory files are append-only:
- Never delete entries
- Only add new data
- Full history preserved

This enables:
- Progress analysis over time
- Pattern detection
- Audit trail

### Human Oversight

Claude must get approval before writing:

1. Claude proposes an update
2. Shows you the content
3. You approve or modify
4. Only then is it written

### Source of Truth

Memory files are authoritative:

```
.claude/memory/*    ←── Source of truth
        │
        ▼
paths/Advanced/tracker.md  ←── Derived artifact
```

The tracker can be regenerated anytime from memory.

---

## File Details

### learner_profile.json

Your goals, constraints, and preferences.

```json
{
  "level": "Advanced",
  "goals": [
    "Master ML engineering end-to-end",
    "Build production RAG systems"
  ],
  "constraints": {
    "hours_per_week": 15,
    "preferred_times": ["evenings", "weekends"]
  },
  "schedule": {
    "start_date": "2026-01-01",
    "current_month": 1,
    "current_week": 1
  }
}
```

**When updated**:
- Initial setup
- Schedule changes
- Goal updates

### progress_log.jsonl

Timestamped events in your journey.

```json
{"timestamp": "2026-01-15T10:00:00Z", "event": "week_start", "week": 3}
{"timestamp": "2026-01-19T17:00:00Z", "event": "week_complete", "status": "complete"}
{"timestamp": "2026-01-20T14:00:00Z", "event": "deliverable_shipped", "name": "baseline_model"}
```

**Event types**:
- `week_start` — New week begins
- `week_complete` — Week finished
- `deliverable_shipped` — Project milestone
- `blocker_identified` — Something blocking
- `blocker_resolved` — Block overcome
- `path_change` — Adaptation applied

### decisions.jsonl

Important decisions with rationale.

```json
{"timestamp": "2026-02-01T10:00:00Z", "decision": "skip_remediation", "rationale": "Score 7.5 sufficient"}
{"timestamp": "2026-03-15T14:00:00Z", "decision": "project_swap", "from": "forecaster", "to": "predictor"}
```

**Decision types**:
- `level_selected` — Initial level choice
- `skip_remediation` — Chose not to remediate
- `project_swap` — Changed project
- `level_change` — Upgraded/downgraded

### best_practices.md

Living document of learnings.

```markdown
# Best Practices

## 2026-01-20 — Focus Management

Taking 5-minute breaks every 45 minutes helps maintain focus.

## 2026-02-05 — Debugging Embeddings

When debugging embedding issues, check input encoding first.
```

**When updated**:
- During retros
- After solving problems
- Using `/add-best-practice`

---

## How Claude Uses Memory

### Reading

Claude reads memory to provide context:

```python
# Evaluate progress
progress = load_jsonl("progress_log.jsonl")
completed_weeks = [e for e in progress if e.get("event") == "week_complete"]
```

### Proposing Writes

Claude never writes directly. Instead:

```
Claude: I'd like to log your week completion. Here's the proposed entry:

{
  "timestamp": "2026-01-26T17:00:00Z",
  "event": "week_complete",
  "week": 4,
  "status": "complete"
}

Approve this entry?
```

### After Approval

Only after you confirm:

```
You: Yes, approve.

Claude: ✓ Entry added to progress_log.jsonl
```

---

## Your Control

You have full control over memory:

### View Memory

```bash
cat .claude/memory/learner_profile.json
cat .claude/memory/progress_log.jsonl
cat .claude/memory/best_practices.md
```

### Edit Memory

You can edit files directly:
- Fix mistakes
- Add entries manually
- Update profile

### Reset Memory

If needed, you can clear and restart:

```bash
# Backup first!
cp -r .claude/memory .claude/memory.backup

# Clear progress (keep profile)
echo "" > .claude/memory/progress_log.jsonl
echo "" > .claude/memory/decisions.jsonl
```

---

## Integration with Path Engine

The path engine uses memory for:

### evaluate.py

Reads:
- `progress_log.jsonl` — Count events, check consistency
- `learner_profile.json` — Get current position
- `best_practices.md` — Count entries

Outputs: Scores and recommendations

### adapt.py

Reads:
- Evaluation results
- `decisions.jsonl` — Past decisions

Outputs: Proposals (not applied automatically)

### report.py

Reads:
- All memory files

Outputs: `paths/Advanced/tracker.md` (with confirmation)

---

## Best Practices for Memory

### Log Regularly

Add entries often, even brief ones:

```json
{"timestamp": "2026-01-20T10:00:00Z", "event": "task_complete", "task": "wrote tests"}
```

### Keep JSON Valid

For `.jsonl` files, each line must be valid JSON.

### Capture Insights

When something works, add to best practices:

```
/add-best-practice — Morning sessions are more productive.
```

### Review Periodically

Look back at your journey:

```bash
wc -l .claude/memory/progress_log.jsonl  # How many events?
head -20 .claude/memory/progress_log.jsonl  # Early entries
tail -20 .claude/memory/progress_log.jsonl  # Recent entries
```

---

## Troubleshooting

### Tracker looks wrong

Regenerate from memory:
```bash
python .claude/path-engine/report.py
```

### Progress log corrupted

Check for invalid JSON:
```python
import json
with open('.claude/memory/progress_log.jsonl') as f:
    for i, line in enumerate(f, 1):
        try:
            json.loads(line)
        except:
            print(f"Invalid line {i}: {line}")
```

### Need to undo an entry

JSON Lines files are append-only, but you can:
1. Back up the file
2. Remove the bad line
3. Note the edit in a new entry

---

## Links

- [Memory files](../.claude/memory/)
- [Path engine](../.claude/path-engine/)
- [System overview](system-overview.md)
