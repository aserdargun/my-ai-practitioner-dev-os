# Agents Guide

How to work with Claude Code's advisory agents.

---

## Overview

Agents are roles Claude assumes when helping you. Each agent has:

- Specific focus area
- Defined responsibilities
- Constraints on actions
- Commands they handle

---

## Available Agents

### Planner Agent

**Focus**: Scheduling and planning

**Responsibilities**:
- Create weekly plans
- Suggest task prioritization
- Propose schedule adjustments
- Identify dependencies

**Commands**: `/plan-week`, `/start-week`

**Invoke with**:
```
Act as the Planner agent and help me break down this month's goals.
```

### Builder Agent

**Focus**: Implementation

**Responsibilities**:
- Propose code implementations
- Suggest architecture patterns
- Help with debugging
- Create documentation

**Commands**: `/ship-mvp`, `/publish`

**Invoke with**:
```
As the Builder, implement the embedding pipeline for my RAG service.
```

### Reviewer Agent

**Focus**: Quality and feedback

**Responsibilities**:
- Review code quality
- Check documentation
- Validate test coverage
- Suggest improvements

**Commands**: `/harden`

**Invoke with**:
```
Act as the Reviewer and check my API implementation for issues.
```

### Evaluator Agent

**Focus**: Assessment

**Responsibilities**:
- Compute progress scores
- Identify patterns
- Generate reports
- Propose adaptations

**Commands**: `/status`, `/evaluate`, `/adapt-path`

**Invoke with**:
```
As the Evaluator, assess my progress for this month.
```

### Coach Agent

**Focus**: Guidance and support

**Responsibilities**:
- Diagnose learning blocks
- Facilitate retrospectives
- Suggest strategies
- Provide encouragement

**Commands**: `/retro`, `/add-best-practice`, `/debug-learning`

**Invoke with**:
```
Act as the Coach and help me understand why I'm procrastinating.
```

### Researcher Agent

**Focus**: Investigation

**Responsibilities**:
- Research technologies
- Find resources
- Compare approaches
- Synthesize information

**Commands**: (No dedicated commands)

**Invoke with**:
```
As the Researcher, compare Pinecone and Qdrant for my use case.
```

---

## Human-in-the-Loop

**Critical**: All agents must get your approval before taking action.

### What Agents Do

- Provide recommendations
- Draft plans and code
- Suggest changes
- Offer guidance

### What Agents Don't Do

- Automatically modify files
- Commit without permission
- Change your learning path
- Make decisions for you

### The Approval Flow

```
Agent proposes ──► You review ──► You approve ──► Action taken
                       │
                       ├──► You modify ──► You approve ──► Action taken
                       │
                       └──► You reject ──► No action
```

---

## Agent Handoffs

Agents can suggest handoffs to other agents:

| From | To | When |
|------|-----|------|
| Planner | Builder | Plan approved, ready to implement |
| Builder | Reviewer | MVP shipped, ready for review |
| Reviewer | Coach | Review reveals learning gaps |
| Coach | Researcher | Need deep investigation |
| Researcher | Builder | Research complete, ready to implement |
| Evaluator | Planner | Evaluation done, ready to re-plan |

**Handoffs require your confirmation.**

Example:
```
I've completed the code review. I noticed some knowledge gaps around
transformers. Would you like me to hand off to the Coach agent
to help debug your learning?
```

---

## Tips for Working with Agents

### Be Specific

Give context for better results:

```
Act as the Planner. I have 10 hours this week, I'm behind on Month 3,
and I need to ship the retrieval API by Friday.
```

### Request Agent Explicitly

If you want a specific perspective:

```
As the Reviewer, focus only on security issues in my code.
```

### Combine Agents

You can request multi-agent workflows:

```
First, act as the Planner to create a plan.
Then, as the Builder, help me implement step 1.
```

### Trust the Process

Each agent brings a different perspective:
- Planner helps you be realistic about time
- Builder helps you ship
- Reviewer helps you improve
- Coach helps you grow

---

## Agent Files

Full agent specifications are in:

- [.claude/agents/planner.md](../.claude/agents/planner.md)
- [.claude/agents/builder.md](../.claude/agents/builder.md)
- [.claude/agents/reviewer.md](../.claude/agents/reviewer.md)
- [.claude/agents/evaluator.md](../.claude/agents/evaluator.md)
- [.claude/agents/coach.md](../.claude/agents/coach.md)
- [.claude/agents/researcher.md](../.claude/agents/researcher.md)

See [.claude/agents/README.md](../.claude/agents/README.md) for the overview.
