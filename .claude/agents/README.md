# Agents

This folder contains the advisory role definitions for Claude Code. Each agent has specific responsibilities, constraints, and recommended handoffs.

## Overview

Agents are advisory roles that Claude assumes when helping you with your learning journey. Each agent:

- Has a specific focus area
- Provides recommendations (not automatic actions)
- Requires your explicit approval before making changes
- Can hand off to other agents when appropriate

## Available Agents

| Agent | Role | Primary Commands |
|-------|------|------------------|
| [Planner](planner.md) | Suggests plans; user approves before execution | `/plan-week`, `/start-week` |
| [Builder](builder.md) | Proposes implementations; user reviews and approves | `/ship-mvp` |
| [Reviewer](reviewer.md) | Provides feedback; user decides what to act on | `/harden` |
| [Evaluator](evaluator.md) | Generates assessments; user validates results | `/evaluate` |
| [Coach](coach.md) | Offers guidance; user chooses which advice to follow | `/debug-learning`, `/retro` |
| [Researcher](researcher.md) | Gathers information; user directs research focus | General research tasks |

## Human-in-the-Loop Requirement

**Critical**: Each agent must:

1. Present recommendations to the user
2. Wait for explicit approval before taking any action
3. Only modify files, state, or learning path after user confirmation
4. Confirm agent handoffs with the user

## Invoking Agents

You can invoke agents directly in Claude Code:

```
Act as the Planner agent and help me plan my week.
```

Or through commands that route to specific agents:

```
/plan-week
```

## Agent Handoffs

Agents may suggest handoffs to other agents. For example:

- Planner → Builder (after plan is approved)
- Builder → Reviewer (after MVP is shipped)
- Reviewer → Coach (if learning blockers are identified)

All handoffs require your confirmation.

## Adding New Agents

To add a new agent:

1. Create a new `.md` file in this folder
2. Follow the template structure (see existing agents)
3. Update this README
4. Update `../commands/catalog.md` if the agent handles new commands
