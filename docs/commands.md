# Commands Guide

User-friendly guide to all available slash commands.

---

## Quick Reference

| Command | Purpose | Agent |
|---------|---------|-------|
| `/status` | Check current progress | Evaluator |
| `/plan-week` | Create weekly plan | Planner |
| `/start-week` | Initialize week templates | Planner |
| `/ship-mvp` | Get MVP guidance | Builder |
| `/harden` | Add tests and polish | Reviewer |
| `/publish` | Prepare for demo/write-up | Builder |
| `/retro` | Weekly retrospective | Coach |
| `/evaluate` | Compute progress scores | Evaluator |
| `/adapt-path` | Get path change proposals | Evaluator |
| `/add-best-practice` | Capture a learning | Coach |
| `/debug-learning` | Troubleshoot blocks | Coach |

---

## Planning Commands

### /status

Check your current learning status.

**When to use**: Start of day, when feeling lost, before planning.

**Example**:
```
/status
```

**Output**: Progress summary, current blockers, recommended next actions.

### /plan-week

Create a weekly learning plan.

**When to use**: Every Monday (or week start).

**Example**:
```
/plan-week — I have 12 hours this week, want to focus on the embedding pipeline.
```

**Output**: Draft weekly plan with daily tasks and time estimates.

### /start-week

Initialize the week with templates.

**When to use**: After approving your week plan.

**Example**:
```
/start-week
```

**Output**: Creates journal entry, updates tracker.

---

## Building Commands

### /ship-mvp

Get guidance on shipping minimum viable product.

**When to use**: When starting a deliverable, when scope feels too large.

**Example**:
```
/ship-mvp — I need to ship the retrieval API by Friday.
```

**Output**: MVP scope, implementation steps, Definition of Done checklist.

### /harden

Review and improve code quality.

**When to use**: After MVP, before publishing.

**Example**:
```
/harden — Review my RAG service for quality and security.
```

**Output**: Code review feedback, test recommendations, documentation gaps.

### /publish

Prepare for demo and write-up.

**When to use**: End of month, when adding to portfolio.

**Example**:
```
/publish — I want to create a Medium post about this project.
```

**Output**: Demo script, write-up draft, portfolio entry.

---

## Reflection Commands

### /retro

Run a weekly retrospective.

**When to use**: Every Friday (or week end).

**Example**:
```
/retro
```

**Output**: Reflection prompts, summary of what worked/didn't, action items.

### /add-best-practice

Capture a learning insight.

**When to use**: When you discover something useful.

**Example**:
```
/add-best-practice — Using fixtures for vector store setup saves time.
```

**Output**: Formatted entry for approval, added to best_practices.md.

### /debug-learning

Troubleshoot learning blocks.

**When to use**: When stuck for more than a day.

**Example**:
```
/debug-learning — I've been stuck on attention mechanisms for 3 days.
```

**Output**: Diagnosis of block type, strategies to overcome, resources.

---

## Evaluation Commands

### /evaluate

Compute progress scores.

**When to use**: End of week, end of month.

**Example**:
```
/evaluate
```

**Output**: Scores across dimensions, trend analysis, recommendations.

### /adapt-path

Get path change proposals.

**When to use**: After evaluation, when considering changes.

**Example**:
```
/adapt-path
```

**Output**: Proposed adaptations with rationale and impact.

---

## Common Workflows

### Monday Start

```
/status
/plan-week
/start-week
```

### Friday End

```
/retro
/evaluate
```

### End of Month

```
/harden
/publish
/evaluate
/adapt-path
```

### When Stuck

```
/debug-learning
/status
/plan-week  (adjusted)
```

---

## Tips

### Be Specific

Add context to get better results:

```
/plan-week — I have 8 hours, mostly evenings, want to finish the API tests.
```

### Chain Commands

Commands work well together:

```
/status → understand where you are
/plan-week → create plan based on status
/start-week → initialize the week
```

### Save Best Practices

When something works, capture it:

```
/add-best-practice — Morning sessions are 2x more productive for me.
```

---

## Full Catalog

For complete command specifications, see:

[.claude/commands/catalog.md](../.claude/commands/catalog.md)

Each command file includes:
- Purpose
- Inputs
- Outputs
- When to use
- Agent routing
- Example usage
