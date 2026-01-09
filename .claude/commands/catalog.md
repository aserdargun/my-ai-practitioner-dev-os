# Command Catalog

Complete reference for all available slash commands in the AI Practitioner Booster 2026 learning system.

---

## Planning Commands

### /status
View current progress and blockers.

- **Agent**: Evaluator
- **Inputs**: None required
- **Outputs**: Progress summary, current blockers, next actions
- **File**: [status.md](status.md)

### /plan-week
Create a weekly learning plan.

- **Agent**: Planner
- **Inputs**: Optional: available hours, focus area
- **Outputs**: Draft weekly plan for approval
- **File**: [plan-week.md](plan-week.md)

### /start-week
Initialize a new week with templates.

- **Agent**: Planner
- **Inputs**: None required
- **Outputs**: Week stub in journal, tracker update
- **File**: [start-week.md](start-week.md)

---

## Building Commands

### /ship-mvp
Get guidance on shipping minimum viable product.

- **Agent**: Builder
- **Inputs**: Current project context
- **Outputs**: MVP scope, implementation steps, DoD checklist
- **File**: [ship-mvp.md](ship-mvp.md)

### /harden
Add tests, docs, and polish.

- **Agent**: Reviewer
- **Inputs**: Current project to review
- **Outputs**: Review feedback, improvement checklist
- **File**: [harden.md](harden.md)

### /publish
Prepare for demo and write-up.

- **Agent**: Builder
- **Inputs**: Completed project
- **Outputs**: Demo script, write-up draft, portfolio entry
- **File**: [publish.md](publish.md)

---

## Reflection Commands

### /retro
Run weekly retrospective.

- **Agent**: Coach
- **Inputs**: None required
- **Outputs**: Retrospective template filled, insights captured
- **File**: [retro.md](retro.md)

### /add-best-practice
Capture a learning insight.

- **Agent**: Coach
- **Inputs**: The best practice or insight
- **Outputs**: Entry appended to best_practices.md (with approval)
- **File**: [add-best-practice.md](add-best-practice.md)

### /debug-learning
Troubleshoot learning blocks.

- **Agent**: Coach
- **Inputs**: Description of the block
- **Outputs**: Diagnosis, recommended strategies
- **File**: [debug-learning.md](debug-learning.md)

---

## Evaluation Commands

### /evaluate
Compute progress scores.

- **Agent**: Evaluator
- **Inputs**: None required
- **Outputs**: Evaluation report with scores
- **File**: [evaluate.md](evaluate.md)

### /adapt-path
Get path change recommendations.

- **Agent**: Evaluator
- **Inputs**: Current evaluation results
- **Outputs**: Proposed adaptations (for approval)
- **File**: [adapt-path.md](adapt-path.md)

---

## Command Quick Reference

```
/status              → See where you are
/plan-week           → Plan your week
/start-week          → Initialize week templates
/ship-mvp            → Ship minimum viable product
/harden              → Add tests and polish
/publish             → Prepare for demo/write-up
/retro               → Weekly retrospective
/add-best-practice   → Capture insight
/debug-learning      → Troubleshoot blockers
/evaluate            → Compute scores
/adapt-path          → Get adaptation proposals
```

---

## Typical Workflows

### Weekly Flow
```
Monday:     /plan-week → /start-week
Tue-Thu:    /ship-mvp → /harden
Friday:     /retro → /evaluate
```

### Monthly Flow
```
Week 1-3:   Build and iterate
Week 4:     /publish → /evaluate → /adapt-path
```

### When Stuck
```
/debug-learning → /status → /plan-week (adjusted)
```
