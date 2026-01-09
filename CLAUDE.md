# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is an **AI Practitioner Booster 2026** - a generator repository that creates a personalized, AI-driven learning system. Users fork this repo and run the generator prompt to create their custom learning OS.

## How Generation Works

### Option A: Full Curriculum
1. User runs: `Execute @SETUP.md`
2. Claude asks for learner level
3. Claude uses `STACK.md` (all items unchecked = full curriculum for selected tiers)

### Option B: Custom Stack
1. User edits `MY_STACK.md`, checking `[x]` desired technologies
2. User runs: `Execute @SETUP.md for @MY_STACK.md`
3. Claude asks for learner level
4. Claude uses only checked items from `MY_STACK.md`

## Learner Levels (Pace-Based, Cumulative)

- **Beginner**: Tier 1 technologies only
- **Intermediate**: Tier 1 + Tier 2 technologies
- **Advanced**: Tier 1 + Tier 2 + Tier 3 technologies

## Key Files

| File | Purpose |
|------|---------|
| `SETUP.md` | Generator prompt - the canonical source for repo generation |
| `STACK.md` | Default tech stack (all 175 items unchecked - full curriculum) |
| `MY_STACK.md` | Custom tech stack (user checks desired items) |
| `README.md` | User-facing documentation for setup and usage |

## After Generation - Expected Structure

The generated repo will contain:
- `.claude/` - Claude capabilities (agents, commands, skills, hooks, memory, MCP, path-engine)
- `docs/` - System documentation and guides
- `paths/{{LEARNER_LEVEL}}/` - Learner dashboard with 12-month curriculum
- `stacks/` - Tier definitions
- `templates/` - Runnable project templates (FastAPI, data pipeline, RAG, eval harness)
- `.github/workflows/ci.yml` - GitHub Actions (ruff + pytest)

## Human-in-the-Loop Requirement

All agents provide recommendations that require explicit user approval before execution. The evaluation loop is: Evaluate → Present recommendations → **User approves** → Execute.

## Memory System

After generation, `.claude/memory/` files are append-only sources of truth:
- `learner_profile.json` - Goals, constraints, and schedule
- `progress_log.jsonl` - Timestamped events
- `decisions.jsonl` - Important decisions
- `best_practices.md` - Living doc

`paths/{{LEARNER_LEVEL}}/tracker.md` is a derived artifact that `report.py` may regenerate.

## Path Engine Commands (Post-Generation)

```bash
python .claude/path-engine/evaluate.py   # Compute scores
python .claude/path-engine/adapt.py      # Propose adaptations (user approves)
python .claude/path-engine/report.py     # Update tracker
```

## Allowed Adaptations

The system can only propose these changes (user must approve):
- Change learner level (Beginner ↔ Intermediate ↔ Advanced)
- Reorder upcoming months within tier scope
- Insert remediation weeks
- Swap month project for equivalent scope alternative
