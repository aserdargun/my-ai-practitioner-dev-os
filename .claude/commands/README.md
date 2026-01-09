# Commands

This folder contains Claude Code slash commands for the AI Practitioner Booster 2026 learning system.

## Overview

Commands are shortcuts you can invoke in Claude Code to trigger specific workflows. Each command:

- Has a dedicated `.md` file defining its behavior
- Routes to a specific agent
- Produces defined outputs
- Follows the human-in-the-loop principle

## Available Commands

See [catalog.md](catalog.md) for the complete command reference.

| Command | Purpose | Agent |
|---------|---------|-------|
| `/status` | View current progress and blockers | Evaluator |
| `/plan-week` | Create weekly learning plan | Planner |
| `/start-week` | Initialize week with templates | Planner |
| `/ship-mvp` | Get guidance on shipping MVP | Builder |
| `/harden` | Add tests, docs, and polish | Reviewer |
| `/publish` | Prepare for demo and write-up | Builder |
| `/retro` | Run weekly retrospective | Coach |
| `/evaluate` | Compute progress scores | Evaluator |
| `/adapt-path` | Get path change recommendations | Evaluator |
| `/add-best-practice` | Capture a learning insight | Coach |
| `/debug-learning` | Troubleshoot learning blocks | Coach |

## Usage

In Claude Code, type the command:

```
/status
```

Or with additional context:

```
/plan-week — I have 15 hours available this week and want to focus on the vector database integration.
```

## Command File Format

Each command file follows this structure:

```markdown
# Command: /command-name

## Purpose
[What this command does]

## Inputs
[What the user needs to provide, if any]

## Outputs
[What artifacts or results are produced]

## When to Use
[Scenarios when this command is appropriate]

## Agent Routing
[Which agent handles this command]

## Example Usage
[Copy-paste example prompt for the user]
```

## Adding New Commands

To add a new command:

1. Create a new `.md` file in this folder (e.g., `my-command.md`)
2. Follow the command file format
3. Add the command to `catalog.md`
4. Update `docs/commands.md` with user-friendly documentation

## Human-in-the-Loop

All commands follow the approval workflow:

1. Command generates recommendations or drafts
2. You review the output
3. You approve or modify as needed
4. Only approved changes are applied
