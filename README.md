# ai-practitioner-dev-os

**AI Practitioner Booster 2026 — AI-driven, project-based learning system**

A public, forkable GitHub repository that creates a personalized learning operating system for AI practitioners. This system guides you through a 12-month curriculum with AI-assisted evaluation, adaptation, and human-approved path changes.

---

## What This Repo Is

This is a **learning OS** that combines:
- **Structured curriculum**: 12 months of project-based learning
- **AI assistance**: Claude Code acts as your advisor (planner, builder, reviewer, evaluator, coach, researcher)
- **Human-in-the-loop**: All recommendations require your explicit approval before execution
- **Adaptive paths**: The system proposes adjustments based on your progress—you decide what to accept

---

## How to Use (From Zero)

1. **Fork this repository** to your GitHub account
2. **Connect Claude Code** to your forked repository
3. **Run the generator** (if starting fresh):
   ```
   Execute @SETUP.md
   ```
   Or with a custom stack:
   ```
   Execute @SETUP.md for @MY_STACK.md
   ```
4. **Clone your generated repository** to your local dev environment
5. **Recommended IDE**: VS Code with Claude Code extension

> See [SETUP.md](SETUP.md) for the canonical generator prompt.

---

## Quickstart (5 Minutes)

Run your first evaluation cycle:

```bash
# 1. Check your current status
/status

# 2. Plan your week
/plan-week

# 3. Run evaluation
python .claude/path-engine/evaluate.py

# 4. Generate progress report
python .claude/path-engine/report.py
```

---

## How the AI-Assisted Loop Works

```
┌─────────────┐     ┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Evaluate   │ ──► │  Recommend  │ ──► │ User Approves│ ──► │   Execute   │
└─────────────┘     └─────────────┘     └──────────────┘     └─────────────┘
       ▲                                                            │
       └────────────────────────────────────────────────────────────┘
```

**Key principle**: No changes happen without your explicit approval. Claude provides suggestions; you make final decisions.

---

## Your Learning Dashboard

**Your level**: Advanced

**Go to your dashboard**: [paths/Advanced/README.md](paths/Advanced/README.md)

This is your main control center with:
- Current month progress
- Weekly planning templates
- Commands cheat-sheet
- Evaluation snapshots

---

## Daily Workflow

1. Open your dashboard: `paths/Advanced/README.md`
2. Check today's focus from your week plan
3. Work on your project deliverables
4. Log progress: `/add-best-practice` for insights learned
5. Ask Claude for help when stuck: `/debug-learning`

## Weekly Workflow

| Day | Activity |
|-----|----------|
| **Monday** | `/plan-week` - Set goals for the week |
| **Tue-Thu** | Build, learn, iterate |
| **Friday** | `/retro` - Reflect on the week |
| **End of Week** | `/evaluate` - Check progress signals |

---

## How to Ask Claude for Help

Use `/commands` to see all available commands:

| Command | Purpose |
|---------|---------|
| `/status` | View current progress and blockers |
| `/plan-week` | Create weekly learning plan |
| `/start-week` | Initialize week with templates |
| `/ship-mvp` | Get guidance on shipping minimum viable product |
| `/harden` | Add tests, docs, and polish |
| `/publish` | Prepare for demo and write-up |
| `/retro` | Run weekly retrospective |
| `/evaluate` | Compute progress scores |
| `/adapt-path` | Get path change recommendations |
| `/add-best-practice` | Capture a learning insight |
| `/debug-learning` | Troubleshoot learning blocks |

See [docs/commands.md](docs/commands.md) for detailed documentation.

---

## Where Claude Capabilities Live

All Claude Code capabilities are in the `.claude/` folder:

```
.claude/
├── agents/          # Advisory roles (planner, builder, reviewer, etc.)
├── commands/        # Slash commands (/status, /plan-week, etc.)
├── skills/          # Reusable playbooks (EDA, RAG, forecasting, etc.)
├── hooks/           # Automation scripts (pre/post week, publish checks)
├── memory/          # Learning state (profile, progress, decisions)
├── mcp/             # Tool contracts and server stubs
└── path-engine/     # Evaluation and adaptation scripts
```

See [.claude/README.md](.claude/README.md) for full documentation.

---

## Repository Structure

```
/
├── README.md                    # This file
├── CLAUDE.md                    # Claude Code instructions
├── SETUP.md                     # Generator prompt
├── STACK.md                     # Full tech stack (175 items)
├── MY_STACK.md                  # Your custom stack selections
├── .claude/                     # Claude capabilities
├── docs/                        # System documentation
├── stacks/                      # Tier definitions
├── paths/Advanced/              # Your 12-month curriculum
├── templates/                   # Project templates
├── examples/                    # Reference implementations
└── .github/                     # CI/CD and issue templates
```

---

## Links

- **Generator Prompt**: [SETUP.md](SETUP.md)
- **Your Dashboard**: [paths/Advanced/README.md](paths/Advanced/README.md)
- **Commands Guide**: [docs/commands.md](docs/commands.md)
- **How to Use**: [docs/how-to-use.md](docs/how-to-use.md)
- **Evaluation Rubric**: [docs/evaluation/rubric.md](docs/evaluation/rubric.md)

---

## License

This project is open source. Fork it, customize it, and build your AI practitioner skills.
