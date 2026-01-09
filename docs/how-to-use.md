# How to Use

Complete guide for using the AI Practitioner Booster 2026 learning system.

---

## Overview

This learning OS helps you build AI/ML skills through:

1. **Structured curriculum** — 12 months of project-based learning
2. **AI assistance** — Claude Code as your advisor
3. **Adaptive path** — System proposes adjustments based on progress
4. **Human control** — You approve all changes

---

## Running the System Loop

### Locally (Scripts)

From the repository root:

```bash
# Evaluate your progress
python .claude/path-engine/evaluate.py

# Get adaptation proposals
python .claude/path-engine/adapt.py

# Update your tracker
python .claude/path-engine/report.py
```

### Via Claude Code

Use slash commands:

```
/status       # Quick status check
/evaluate     # Compute scores
/adapt-path   # Get proposals
```

---

## Weekly Cadence

Each month has 4 weeks with distinct focuses:

### Week 1 — Learn & Plan

- Review month goals
- Study core concepts
- Set up project scaffold
- `/plan-week` to create your plan
- `/start-week` to initialize templates

### Week 2 — Build

- Implement core features
- Write tests as you go
- Log progress daily
- `/ship-mvp` when ready for MVP

### Week 3 — Iterate

- Add remaining features
- Improve based on feedback
- Address edge cases
- `/harden` to polish

### Week 4 — Ship & Reflect

- Complete documentation
- Prepare demo
- Run retrospective
- `/publish` to prepare showcase
- `/retro` to reflect
- `/evaluate` to assess progress

---

## Logging Progress & Reflections

### Daily Logging

Add entries to your week's journal:

```
paths/Advanced/journal/YYYY-wWW.md
```

Or use the hook:

```bash
bash .claude/hooks/post_week_review.sh
```

### Progress Events

Events are logged to `.claude/memory/progress_log.jsonl`:

```json
{"timestamp": "2026-01-15T10:00:00Z", "event": "deliverable_shipped", "name": "baseline_model"}
```

### Reflections

Weekly retros are captured through:

1. `/retro` command
2. Journal entries in `paths/Advanced/journal/`
3. Best practices in `.claude/memory/best_practices.md`

---

## Requesting Path Changes

### Automatic Proposals

After running `/evaluate`, check for proposals:

```
/adapt-path
```

The system may propose:
- Level change (Beginner ↔ Intermediate ↔ Advanced)
- Month reordering
- Remediation week
- Project swap

### Manual Requests

You can request changes directly:

```
I'd like to swap Month 5's project. Can you propose an alternative?
```

or

```
I feel the pace is too fast. Can we consider a remediation week?
```

### Approval Process

1. System proposes a change
2. You review the impact
3. You explicitly approve or reject
4. Only approved changes are applied

---

## Capturing Best Practices

### Using the Command

```
/add-best-practice — Taking breaks every 45 minutes helps me focus.
```

### Manually

Edit `.claude/memory/best_practices.md`:

```markdown
## 2026-01-20 — Focus Management

Taking 5-minute breaks every 45 minutes helps maintain focus during long coding sessions.
```

### When to Capture

- After solving a tricky problem
- When you discover a useful pattern
- During retrospectives
- When a technique works well

---

## Memory System

### Files

| File | Purpose |
|------|---------|
| `learner_profile.json` | Your goals and constraints |
| `progress_log.jsonl` | Timestamped events |
| `decisions.jsonl` | Important decisions |
| `best_practices.md` | Learnings captured |

### Source of Truth

Memory files (`.claude/memory/*`) are the source of truth.

The tracker (`paths/Advanced/tracker.md`) is a derived artifact that can be regenerated.

### Editing Memory

You can directly edit memory files, but prefer:
- Using commands that propose updates
- Appending (not modifying) existing entries
- Keeping the JSON valid

---

## Command Reference

| Command | When to Use |
|---------|-------------|
| `/status` | Start of day, when lost |
| `/plan-week` | Monday, start of week |
| `/start-week` | After plan approved |
| `/ship-mvp` | When ready to ship minimal version |
| `/harden` | Before publishing |
| `/publish` | End of month |
| `/retro` | End of week |
| `/evaluate` | End of week/month |
| `/adapt-path` | After evaluation |
| `/add-best-practice` | When you learn something |
| `/debug-learning` | When stuck |

---

## Invoking Agents

Ask Claude to act as a specific agent:

```
Act as the Planner agent and help me break down this month's goals.
```

```
As the Coach, help me understand why I'm procrastinating on Kubernetes.
```

```
As the Builder, implement the embedding pipeline step-by-step.
```

---

## Troubleshooting

### Commands not working

Ensure you're in Claude Code with the repo connected.

### Hooks fail on Windows

Use WSL or Git Bash. See `docs/hooks.md` for manual fallback.

### Tracker looks wrong

Regenerate with:
```bash
python .claude/path-engine/report.py
```

### Evaluation seems off

Check that your progress log has recent entries:
```bash
tail -10 .claude/memory/progress_log.jsonl
```

---

## Next Steps

1. Open your dashboard: `paths/Advanced/README.md`
2. Run `/status` to see where you are
3. Run `/plan-week` to plan your week
4. Start building!
