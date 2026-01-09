# System Overview

Architecture and design of the AI Practitioner Booster 2026 learning system.

---

## What This System Is

The AI Practitioner Booster 2026 is a **learning operating system** that:

1. Provides structured, project-based curriculum
2. Uses AI (Claude Code) as an advisor
3. Adapts to your progress and needs
4. Keeps you in control of all decisions

---

## The End-to-End Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                        LEARNING LOOP                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│   │  Learn   │───►│  Build   │───►│  Ship    │───►│ Reflect  │ │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│        │                                               │        │
│        │              ┌──────────┐                     │        │
│        └──────────────│  Memory  │◄────────────────────┘        │
│                       └──────────┘                              │
│                            │                                    │
│                            ▼                                    │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│   │ Evaluate │◄───│  Score   │───►│  Adapt   │───►│  Report  │ │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│                                        │                        │
│                                        ▼                        │
│                              ┌────────────────┐                 │
│                              │ User Approves  │                 │
│                              └────────────────┘                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Daily/Weekly Loop

1. **Learn** — Study concepts from the month curriculum
2. **Build** — Work on project deliverables
3. **Ship** — Complete features, run tests, document
4. **Reflect** — Log progress, run retros, capture best practices

### Evaluation Loop

1. **Evaluate** — `evaluate.py` reads memory and computes scores
2. **Score** — Dimensions: completion, quality, consistency, depth, reflection
3. **Adapt** — `adapt.py` proposes changes based on scores
4. **Report** — `report.py` generates tracker
5. **User Approves** — You decide which proposals to accept

---

## System Components

### Claude Capabilities (`.claude/`)

The brain of the system. See [.claude/README.md](../.claude/README.md).

```
.claude/
├── agents/       # Advisory roles (planner, builder, etc.)
├── commands/     # Slash commands (/status, /evaluate, etc.)
├── skills/       # Reusable playbooks
├── hooks/        # Automation scripts
├── memory/       # Learning state
├── mcp/          # Tool contracts
└── path-engine/  # Evaluation & adaptation
```

### Documentation (`docs/`)

User-facing guides (you're reading one now).

### Curriculum (`paths/Advanced/`)

Your learning dashboard and 12-month curriculum.

### Templates (`templates/`)

Runnable project templates to bootstrap your work.

### Stacks (`stacks/`)

Technology tier definitions based on your selections.

---

## Human-in-the-Loop Principle

**Critical design principle**: The system advises, you decide.

### What the System Does

- Computes progress scores
- Proposes adaptations
- Suggests next steps
- Provides templates and playbooks

### What the System Never Does

- Automatically modify your learning path
- Commit changes without permission
- Override your decisions
- Hide information from you

### The Approval Flow

```
Claude proposes → You review → You approve → Changes applied
                     ↓
              You modify → You approve → Changes applied
                     ↓
              You reject → No changes
```

---

## Data Flow

### Memory as Source of Truth

```
┌─────────────────────────────────────────────────────┐
│                  .claude/memory/                    │
│                                                     │
│  ┌──────────────────┐  ┌──────────────────────┐   │
│  │learner_profile   │  │  progress_log.jsonl  │   │
│  │    .json         │  │  (append-only)       │   │
│  └────────┬─────────┘  └──────────┬───────────┘   │
│           │                       │                │
│  ┌────────┴─────────┐  ┌──────────┴───────────┐   │
│  │decisions.jsonl   │  │  best_practices.md   │   │
│  │(append-only)     │  │  (append-only)       │   │
│  └──────────────────┘  └──────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │  path-engine        │
              │  (evaluate, adapt,  │
              │   report)           │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │  tracker.md         │
              │  (derived artifact) │
              └─────────────────────┘
```

### Append-Only Memory

Memory files are append-only:
- Never delete entries
- History is preserved
- Enables analysis and audit

### Derived Artifacts

The tracker (`paths/Advanced/tracker.md`) is derived from memory:
- Can be regenerated anytime
- Don't edit directly
- Memory is authoritative

---

## Agents and Commands

### Agent Roles

| Agent | Focus | Key Commands |
|-------|-------|--------------|
| Planner | Scheduling and planning | /plan-week, /start-week |
| Builder | Implementation | /ship-mvp |
| Reviewer | Quality and feedback | /harden |
| Evaluator | Assessment | /evaluate, /adapt-path |
| Coach | Guidance and support | /retro, /debug-learning |
| Researcher | Investigation | Research tasks |

### Command Routing

Commands route to specific agents:

```
/plan-week  ──► Planner Agent
/ship-mvp   ──► Builder Agent
/harden     ──► Reviewer Agent
/evaluate   ──► Evaluator Agent
/retro      ──► Coach Agent
```

---

## Adaptation System

### Allowed Changes

| Adaptation | Description | Trigger |
|------------|-------------|---------|
| Level change | Upgrade/downgrade level | Score thresholds |
| Month reorder | Swap upcoming months | Dependency issues |
| Remediation week | Insert consolidation time | Low scores |
| Project swap | Replace project | Misalignment |

### Thresholds

| Threshold | Value | Effect |
|-----------|-------|--------|
| Level down | < 5.0 | Suggest downgrade |
| Level up | > 9.0 | Suggest upgrade |
| Remediation | < 6.5 | Suggest extra week |

### Constraints

- Level changes only at month boundaries
- Month reorder preserves tier scope
- Project swaps maintain equivalent scope
- All changes require approval

---

## Getting Started

1. Read [how-to-use.md](how-to-use.md) for practical guidance
2. Open your [dashboard](../paths/Advanced/README.md)
3. Run `/status` to see where you are
4. Follow the weekly cadence

---

## Links

- [Claude Capabilities](../.claude/README.md)
- [Commands Guide](commands.md)
- [Agents Guide](agents.md)
- [Memory System](memory-system.md)
- [Evaluation Rubric](evaluation/rubric.md)
