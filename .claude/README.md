# .claude/ — Claude Code Capabilities

This folder contains all Claude Code capabilities for the AI Practitioner Booster 2026 learning system.

## Overview

The `.claude/` folder is the brain of your learning OS. It contains:

- **Agents**: Advisory roles that help you plan, build, review, evaluate, coach, and research
- **Commands**: Slash commands you can invoke in Claude Code
- **Skills**: Reusable playbooks for common AI/ML tasks
- **Hooks**: Automation scripts for week start/end and publishing
- **Memory**: Your learning state (profile, progress, decisions, best practices)
- **MCP**: Model Context Protocol tool contracts and stubs
- **Path Engine**: Evaluation and adaptation scripts

## Folder Structure

```
.claude/
├── README.md              # This file
├── agents/                # Advisory role definitions
│   ├── README.md
│   ├── planner.md
│   ├── builder.md
│   ├── reviewer.md
│   ├── evaluator.md
│   ├── coach.md
│   └── researcher.md
├── commands/              # Slash commands
│   ├── README.md
│   ├── catalog.md
│   ├── status.md
│   ├── plan-week.md
│   ├── start-week.md
│   ├── ship-mvp.md
│   ├── harden.md
│   ├── publish.md
│   ├── retro.md
│   ├── evaluate.md
│   ├── adapt-path.md
│   ├── add-best-practice.md
│   └── debug-learning.md
├── skills/                # Reusable playbooks
│   ├── README.md
│   ├── eda-to-insight.md
│   ├── baseline-model-and-card.md
│   ├── experiment-plan.md
│   ├── forecasting-checklist.md
│   ├── rag-with-evals.md
│   ├── api-shipping-checklist.md
│   ├── observability-starter.md
│   └── k8s-deploy-checklist.md
├── hooks/                 # Automation scripts
│   ├── README.md
│   ├── pre_week_start.sh
│   ├── post_week_review.sh
│   └── pre_publish_check.sh
├── memory/                # Learning state
│   ├── README.md
│   ├── learner_profile.json
│   ├── progress_log.jsonl
│   ├── decisions.jsonl
│   └── best_practices.md
├── mcp/                   # MCP tool contracts
│   ├── README.md
│   ├── tool-contracts.md
│   ├── examples.md
│   ├── safety.md
│   ├── server_stub/
│   │   ├── README.md
│   │   └── server.py
│   └── client_examples/
│       ├── README.md
│       └── python_client.py
└── path-engine/           # Evaluation & adaptation
    ├── README.md
    ├── evaluate.py
    ├── adapt.py
    └── report.py
```

## Human-in-the-Loop Principle

**Critical**: All agents, commands, and scripts in this folder follow the human-in-the-loop principle:

1. **Evaluate**: Scripts analyze your progress and generate insights
2. **Recommend**: Claude proposes changes or next steps
3. **User Approves**: You review and explicitly approve any changes
4. **Execute**: Only approved changes are applied

No modifications to your learning path, memory, or files happen without your explicit consent.

## Quick Links

- [Agents](agents/README.md) — Advisory roles
- [Commands](commands/catalog.md) — Available slash commands
- [Skills](skills/README.md) — Reusable playbooks
- [Hooks](hooks/README.md) — Automation scripts
- [Memory](memory/README.md) — Learning state
- [MCP](mcp/README.md) — Tool contracts
- [Path Engine](path-engine/README.md) — Evaluation scripts

## Usage

### Invoking Commands

In Claude Code, use slash commands:

```
/status
/plan-week
/evaluate
```

### Running Scripts

From the repository root:

```bash
python .claude/path-engine/evaluate.py
python .claude/path-engine/adapt.py
python .claude/path-engine/report.py
```

### Running Hooks

```bash
bash .claude/hooks/pre_week_start.sh
bash .claude/hooks/post_week_review.sh
bash .claude/hooks/pre_publish_check.sh
```

## Documentation

For full documentation, see:

- [docs/system-overview.md](../docs/system-overview.md) — End-to-end loop explanation
- [docs/commands.md](../docs/commands.md) — Commands guide
- [docs/agents.md](../docs/agents.md) — Agents guide
- [docs/memory-system.md](../docs/memory-system.md) — Memory system guide
