# SETUP.md — Repository Generator Prompt (Claude Code)

## How to use this prompt

### Option A: Full Curriculum
In **Claude Code**, run:
```
Execute @SETUP.md
```
Claude asks your level, then uses `STACK.md` (all items for your level's tiers).

### Option B: Custom Stack
1) Edit `MY_STACK.md` - check `[x]` only technologies you want
2) In **Claude Code**, run:
```
Execute @SETUP.md for @MY_STACK.md
```

Claude will ask **one** question: "What is the learner level? (Beginner / Intermediate / Advanced)"
- **Beginner**: Uses only Tier 1 items
- **Intermediate**: Uses Tier 1 + Tier 2 items
- **Advanced**: Uses Tier 1 + Tier 2 + Tier 3 items

> Important: This prompt is meant to be executed by Claude Code. It is not a human checklist.

### Generator Prompt (copy everything from here to the end)

---

You are Claude Code acting as an **assistant** to the learner in the following advisory roles:
1) a senior AI engineer + OSS maintainer advisor,
2) a learning scientist advisor,
3) a project manager advisor,
4) an evaluator/coach advisor.

**IMPORTANT**: All recommendations, evaluations, and proposed changes require explicit user approval before being applied. Claude provides suggestions; the learner makes final decisions.

Build a public, forkable GitHub repository.

Repo name (use as title in README): "ai-practitioner-dev-os"
Theme: “AI Practitioner Booster 2026 — AI-driven, project-based learning system”.

IMPORTANT: Before you generate anything, ask me ONE question:
- "What is the learner level? (Beginner / Intermediate / Advanced)"
Use the answer to set {{LEARNER_LEVEL}} everywhere.

IMPORTANT: Read the stack file provided by the user (`STACK.md` or `MY_STACK.md`).

**Stack Selection Rules:**

| Learner Level | If items checked `[x]` | If NO items checked (STACK.md default) |
|---------------|------------------------|----------------------------------------|
| **Beginner** | Use checked Tier 1 items only | Use ALL Tier 1 items (53 items) |
| **Intermediate** | Use checked Tier 1 + Tier 2 items | Use ALL Tier 1 + Tier 2 items (148 items) |
| **Advanced** | Use checked items from all tiers | Use ALL items from all tiers (175 items) |

- When items are checked: include ONLY those checked items that match the learner's tier scope
- When NO items are checked: include ALL items from the learner's tier scope
- The tier scope is cumulative: Beginner=T1, Intermediate=T1+T2, Advanced=T1+T2+T3

Hard requirements
- Markdown-first documentation.
- The repo must be immediately usable by a learner (no placeholders except {{LEARNER_LEVEL}}).
- The system must be AI-assisted with human approval, providing recommendations that evolve based on learner successes/failures. All adaptations require explicit learner confirmation before being applied.
- Claude capabilities must live under a `.claude/` folder (agents, commands, skills, hooks, memory, MCP).
- Do not break links from docs/ to tooling; keep docs pointing to `.claude/` where appropriate.
- Provide a “special path README” per learner level that becomes their main dashboard.

Core concept
- Levels are pace-based and cumulative:
  - Beginner completes Tier 1 only in 2026.
  - Intermediate completes Tier 1 + Tier 2 in 2026.
  - Advanced completes Tier 1 + Tier 2 + Tier 3 in 2026 (hands-on across all items).

Allowed adaptations (must be enforced by docs + code)
- Level changes: upgrade/downgrade learner level (Beginner ↔ Intermediate ↔ Advanced), only at month boundaries unless explicitly overridden by rubric rules.
- Month reordering: swap upcoming month modules while preserving tier scope.
- Remediation weeks: insert 1-week remediation blocks inside a month without changing tier scope.
- Project swap: replace a month’s main project with an alternative of equivalent scope/skills (same tier scope), keeping deliverables and DoD comparable.

## Required repository tree (generate exactly this structure)

/ 
  README.md
  CLAUDE.md

  .claude/
    README.md
    agents/
      README.md
      planner.md
      builder.md
      reviewer.md
      evaluator.md
      coach.md
      researcher.md
    commands/
      README.md
      catalog.md
      status.md
      plan-week.md
      start-week.md
      ship-mvp.md
      harden.md
      publish.md
      retro.md
      evaluate.md
      adapt-path.md
      add-best-practice.md
      debug-learning.md
    skills/
      README.md
      eda-to-insight.md
      baseline-model-and-card.md
      experiment-plan.md
      forecasting-checklist.md
      rag-with-evals.md
      api-shipping-checklist.md
      observability-starter.md
      k8s-deploy-checklist.md   # include but gate it to Advanced in docs
    hooks/
      README.md
      pre_week_start.sh
      post_week_review.sh
      pre_publish_check.sh
    memory/
      README.md
      learner_profile.json
      progress_log.jsonl
      decisions.jsonl
      best_practices.md
    mcp/
      README.md
      tool-contracts.md
      examples.md
      safety.md
      server_stub/
        README.md
        server.py
      client_examples/
        README.md
        python_client.py
    path-engine/
      README.md
      evaluate.py
      adapt.py
      report.py

  docs/
    how-to-use.md
    system-overview.md
    commands.md
    agents.md
    skills-playbook.md
    hooks.md
    memory-system.md
    evaluation/
      rubric.md
      signals.md
      scoring.md
      adaptation-rules.md
    publishing/
      how-to-demo.md
      how-to-write-medium-post.md
      portfolio-checklist.md

  stacks/
    tiers.md
    tier-1-beginner.md
    tier-2-intermediate.md
    tier-3-advanced.md

  paths/
    {{LEARNER_LEVEL}}/
      README.md
      tracker.md
      journal/
        README.md
        weekly-template.md
        monthly-template.md
      month-01/
        README.md
      month-02/
        README.md
      month-03/
        README.md
      month-04/
        README.md
      month-05/
        README.md
      month-06/
        README.md
      month-07/
        README.md
      month-08/
        README.md
      month-09/
        README.md
      month-10/
        README.md
      month-11/
        README.md
      month-12/
        README.md

  templates/
    template-fastapi-service/
      README.md
      app/
        main.py
      tests/
        test_health.py
      Dockerfile
      pyproject.toml
    template-data-pipeline/
      README.md
      pipeline/
        run.py
        validate.py
      tests/
        test_validate.py
      pyproject.toml
    template-rag-service/
      README.md
      rag/
        ingest.py
        retrieve.py
        answer.py
      eval/
        golden_set.jsonl
      tests/
        test_retrieve.py
      pyproject.toml
    template-eval-harness/
      README.md
      evals/
        run_evals.py
        graders.py
      datasets/
        sample_golden.jsonl
      pyproject.toml

  examples/
    mini-example/
      README.md
      src/
        README.md
      tests/
        README.md

  .github/
    ISSUE_TEMPLATE/
      bug_report.md
      feature_request.md
      monthly_journal.md
    PULL_REQUEST_TEMPLATE.md
    workflows/
      ci.yml

## Linking rules (do NOT break these)
- docs/commands.md must reference `.claude/commands/catalog.md`
- docs/agents.md must reference `.claude/agents/*.md`
- docs/skills-playbook.md must reference `.claude/skills/*.md`
- docs/hooks.md must reference `.claude/hooks/*.sh`
- docs/memory-system.md must reference `.claude/memory/*`
- docs/evaluation/* must reference `.claude/path-engine/*`
- docs/system-overview.md must explain the end-to-end loop and point to `.claude/README.md`
- paths/{{LEARNER_LEVEL}}/README.md must link to:
  - docs/how-to-use.md
  - stacks/tiers.md
  - docs/commands.md
  - docs/evaluation/rubric.md
  - `.claude/path-engine/report.py` usage
  - `.claude/memory/best_practices.md`

## Content requirements (must be fully written, no empty files)

### 1) Root README.md
Must include:
- What this repo is
- “How to use (from zero)” section:
  1) Fork this repository to your GitHub account
  2) Connect Claude Code to your forked repository
  3) In the README, copy the “Repository Generator Prompt” block and paste it into Claude Code
  4) Claude Code generates the full repo structure and commits it to your fork
  5) Clone your generated repository to your local dev environment
  6) Recommended IDE: VS Code
- Quickstart (5 minutes) to run a first /status + /plan-week + /evaluate + /report cycle
- How the AI-assisted loop works (Evaluate → Recommend → **User Approves** → Execute) — emphasizing that no changes happen without explicit user approval
- Link to learner dashboard: paths/{{LEARNER_LEVEL}}/README.md
- Daily workflow + Weekly workflow
- How to ask Claude for help using /commands
- Where Claude capabilities live: `.claude/`
- Link to `SETUP.md` as the canonical generator prompt (do not duplicate the generator prompt in README to avoid drift)

### 2) paths/{{LEARNER_LEVEL}}/README.md (SPECIAL DASHBOARD)
Must include:
- Learner level shown clearly: {{LEARNER_LEVEL}}
- Current month pointer + checklists
- “This week plan” template
- Commands cheat-sheet (links to docs/commands.md)
- Evaluation snapshot (what to run, how to interpret)
- “If you are stuck” playbook
- “Upgrade/Downgrade rules” and what triggers a path change

### 3) docs/how-to-use.md
Must be ready-to-use, include:
- How to run the system loop locally (scripts + how to invoke via Claude)
- Weekly cadence (Week1/2/3/4)
- How to log progress & reflections
- How to request path changes
- How to capture best practices into `.claude/memory/best_practices.md`

### 4) Commands

IMPORTANT: Claude Code slash commands require individual `.md` files in `.claude/commands/`.
Each command MUST have its own file (e.g., `status.md`, `plan-week.md`, etc.).

Generate these individual command files in `.claude/commands/`:
- `status.md` → /status
- `plan-week.md` → /plan-week
- `start-week.md` → /start-week
- `ship-mvp.md` → /ship-mvp
- `harden.md` → /harden
- `publish.md` → /publish
- `retro.md` → /retro
- `evaluate.md` → /evaluate
- `adapt-path.md` → /adapt-path
- `add-best-practice.md` → /add-best-practice
- `debug-learning.md` → /debug-learning

Each command file MUST follow this format:
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
[Which agent handles this command: Planner, Builder, Reviewer, Evaluator, Coach, or Researcher]

## Example Usage
[Copy-paste example prompt for the user]
```

Additionally:
- `.claude/commands/catalog.md` is the summary/index of all commands.
- `.claude/commands/README.md` explains how to use and extend commands.
- `docs/commands.md` should be a friendly guide and link to the catalog.

### 5) Agents
- `.claude/agents/*.md` define advisory role responsibilities + constraints + recommended handoffs:
  - Planner Agent (suggests plans; user approves before execution)
  - Builder Agent (proposes implementations; user reviews and approves)
  - Reviewer Agent (provides feedback; user decides what to act on)
  - Evaluator Agent (generates assessments; user validates results)
  - Coach Agent (offers guidance; user chooses which advice to follow)
  - Researcher Agent (gathers information; user directs research focus)

**Human-in-the-loop requirement**: Each agent must present recommendations to the user and wait for explicit approval before taking any action that modifies files, state, or learning path. Agent handoffs must be confirmed by the user.

docs/agents.md should explain how to invoke them, the approval workflow, and point to those files.

### 6) Skills
- `.claude/skills/*.md` are the canonical playbooks.
docs/skills-playbook.md summarizes and links.
Each skill must include:
- trigger, steps, artifacts produced, quality bar.

### 7) Hooks
- `.claude/hooks/*.sh` contain runnable (simple) scripts.
docs/hooks.md explains when/why to use them and how.
Hooks required:
- pre_week_start.sh (creates week plan stub, updates tracker)
- post_week_review.sh (prompts retrospective, updates progress log)
- pre_publish_check.sh (runs tests, lints, checks docs links)

Cross-platform note (must appear in docs/hooks.md):
- These hooks are shell scripts intended for Linux/macOS and Windows via WSL or Git Bash.
- Provide a “Manual fallback” subsection showing the equivalent commands a learner can run step-by-step if they cannot run .sh scripts.

### 8) Local "Memory System"
- `.claude/memory/*` is the only "memory store".
Implement:
- learner_profile.json (goals, constraints, schedule)
- progress_log.jsonl (timestamped events)
- decisions.jsonl (important decisions)
- best_practices.md (living doc; appended frequently)

**Human oversight requirement**: Claude must show proposed memory updates to the user and receive explicit approval before writing to any memory file. Memory is for record-keeping, not for autonomously modifying Claude's behavior.

docs/memory-system.md must explain:
- how Claude proposes memory updates (user must approve before write)
- how learner reviews/edits memory (learner has full control)
- how memory informs recommendations (Claude reads memory to provide context-aware suggestions, but user approves all actions)
- IMPORTANT: Memory files are append-only sources of truth; `paths/{{LEARNER_LEVEL}}/tracker.md` is a derived artifact that `report.py` may overwrite/regenerate at any time (with user confirmation).

### 9) Evaluation & Adaptation (Human-Approved)
- `.claude/path-engine/*` implements the recommendation loop with Python stdlib only.
Implement:
- evaluate.py reads `.claude/memory/*` + basic repo signals and outputs scores for user review
- adapt.py **proposes** modifications (repeat month, remediate, accelerate, swap project, reorder upcoming months, change learner level) — **user must explicitly approve each proposed change before it is applied**
- report.py generates a draft report for `paths/{{LEARNER_LEVEL}}/tracker.md` that the user reviews before finalizing

**Critical human-in-the-loop requirement**:
- The evaluation → adaptation → execution flow is: Evaluate → Present recommendations → **User approves** → Execute approved changes only
- adapt.py MUST NOT automatically apply changes; it outputs proposals that require user confirmation
- No path modifications, project swaps, or level changes occur without explicit user approval

Hard rules:
- docs/evaluation/adaptation-rules.md must define the allowed mutations (the "Allowed adaptations" list above), provide a clear schema, and document the user approval workflow.
- adapt.py MUST ONLY output proposed mutations in that schema for user review; changes are only applied after user confirmation.
- docs/evaluation/scoring.md must also include:
  - IMPORTANT: Memory files are append-only sources of truth; `paths/{{LEARNER_LEVEL}}/tracker.md` is a derived artifact that `report.py` may regenerate (with user confirmation).

docs/evaluation/* explain rubric/signals/scoring/adaptation rules, the approval workflow, and link to scripts.

### 10) MCP
- `.claude/mcp/*` contains tool contracts + safety + examples + stubs.
Provide:
- tool-contracts.md (schemas + constraints)
- examples.md (how agents use tools)
- safety.md (secrets, privacy, eval integrity)
Include server stub:
- `.claude/mcp/server_stub/server.py` exposes:
  - hello tool
  - read_repo_file tool (safe subset)
  - write_memory_entry tool (append-only into `.claude/memory/`)
Include a client example:
- `.claude/mcp/client_examples/python_client.py`

### 11) 12-month curriculum
Generate `paths/{{LEARNER_LEVEL}}/month-01..month-12/README.md`.

IMPORTANT: Use the checked items from `STACK.md` to customize each month's curriculum.
- Focus month projects on technologies the user has selected
- If specific technologies are checked, prioritize them in the learning goals
- Distribute the selected technologies across the 12 months appropriately

Each month README MUST include:
- Why it matters (job relevance)
- Prerequisites
- Learning goals (based on selected STACK.md items for this tier)
- Main project (deliverables + Definition of Done checklist)
- Stretch goals
- "Claude prompts" section (copy/paste prompts that call agents + commands)
- How to publish (demo + write-up)
Apply pace rules:
- Beginner: Tier 1 only (use checked Tier 1 items from STACK.md)
- Intermediate: Tier 1 + Tier 2 (use checked items from both tiers)
- Advanced: Tier 1 + Tier 2 + Tier 3 (use checked items from all tiers)
Keep month numbering consistent; Advanced integrates harder infra/ops earlier.

### 12) Stacks
Write:
- stacks/tiers.md (tier definitions + pace)
- stacks/tier-1-beginner.md, tier-2-intermediate.md, tier-3-advanced.md

IMPORTANT: Read the tech stack from `STACK.md` file in the repository root.
- Parse the checked `[x]` items from each tier section
- If no items are checked in STACK.md, use ALL items for that tier as defaults
- Generate the tier files based on the user's selections

The tier structure in STACK.md follows this organization:
- **Tier 1 (Beginner Foundation)**: Mindset & Skills, Algorithms, Languages, Databases, Frameworks, Libraries, Tools & Platforms, Protocols
- **Tier 2 (Intermediate Shipping)**: Skills, Algorithms, Automation, Cloud, Databases, Frameworks, Libraries, Monitoring, Platforms, Services
- **Tier 3 (Advanced Scale/Interop/Perf)**: APIs & Protocols, Systems, Platforms, Performance, Advanced ML, Languages, Domain-Specific

When generating month curricula, prioritize the checked items from STACK.md to create a personalized learning path.

### 13) OSS hygiene + CI
Include:
- GitHub issue templates + PR template
- GitHub Actions workflow (ruff + pytest) on PR and main

### 14) Templates must be real (STRICT)
Each template must have:
- a README explaining usage
- minimal runnable code
- tests that pass
- pyproject.toml with:
  - pinned minimal dependencies (use conservative version ranges)
  - a [tool.ruff] section (or equivalent) with sensible defaults
  - pytest configuration (e.g., [tool.pytest.ini_options]) so tests run consistently
Keep them consistent and lightweight across templates.

### 15) Examples
examples/mini-example must show “done looks like this” with:
- small dataset or stub
- one model or one RAG mini flow
- tests
- demo guide

## Generation rules
- Print the final repo tree first.
- Ensure all relative links work.
- Ensure no file is empty or placeholder (except {{LEARNER_LEVEL}}).
- Prefer simple, standard tooling.
- Add copy/paste “Claude prompts” in each month README that invoke:
  - /commands
  - specific agents
  - memory updates
  - evaluation + adaptation loop
- Make the system feel like a "learning OS" that guides, evaluates, and recommends adaptations — with the learner always in control of final decisions.
- If any instruction conflicts, resolve by priority: Hard requirements → Linking rules → Required tree → Content requirements → Everything else.

Now proceed to generate the entire repository.
