# Command: /plan-week

## Purpose

Create a weekly learning plan based on your monthly goals, available time, and current progress. The plan breaks down the week into actionable tasks with time estimates.

## Inputs

Optional inputs (provide for better planning):
- **Available hours**: How much time you have this week
- **Focus area**: Specific topic or deliverable to prioritize
- **Constraints**: Days off, meetings, or other commitments
- **Preferences**: Morning/evening learning, session length

## Outputs

1. **Weekly Plan Draft** (for your approval)
   - Day-by-day task breakdown
   - Time estimates per task
   - Priority levels
   - Dependencies between tasks

2. **Risk Assessment**
   - Potential blockers
   - Contingency suggestions

## When to Use

- Every Monday (or your week start day)
- After completing a major deliverable
- When priorities shift mid-week
- After a retrospective that identified changes

## Agent Routing

**Planner Agent** handles this command.

The Planner reads from:
- Current month's README (goals and deliverables)
- `.claude/memory/learner_profile.json` (schedule preferences)
- `.claude/memory/progress_log.jsonl` (what's done/in-progress)
- `paths/Advanced/tracker.md` (current status)

## Example Usage

Basic planning:
```
/plan-week
```

With time constraint:
```
/plan-week — I have 12 hours this week, mostly evenings.
```

With focus area:
```
/plan-week — I want to focus on completing the retrieval API and starting evaluations.
```

With full context:
```
/plan-week — 15 hours available, focus on RAG evaluation harness, I'm off Wednesday.
```

## Sample Output

```markdown
## Weekly Plan — Week of March 15, 2026

### Context
- **Available hours**: 12
- **Focus**: Embedding pipeline completion, retrieval API start
- **Current month**: 3 (RAG Systems)

### Plan

#### Monday (2.5 hrs)
- [ ] Review embedding pipeline code (30 min)
- [ ] Implement batch optimization (1.5 hrs)
- [ ] Write batch processing tests (30 min)

#### Tuesday (2.5 hrs)
- [ ] Complete embedding pipeline (1 hr)
- [ ] Start retrieval API scaffold (1.5 hrs)

#### Wednesday (OFF)

#### Thursday (3.5 hrs)
- [ ] Implement basic retrieval endpoint (2 hrs)
- [ ] Add similarity search logic (1.5 hrs)

#### Friday (3.5 hrs)
- [ ] Write retrieval tests (1.5 hrs)
- [ ] Document API contract (1 hr)
- [ ] Weekly retro (30 min)
- [ ] Update tracker (30 min)

### Risks
- Batch optimization might take longer if chunking strategy needs rework
- **Contingency**: Move retrieval tests to next week if needed

### Success Criteria
By end of week:
- [ ] Embedding pipeline fully operational with tests
- [ ] Retrieval API returning results
- [ ] Basic documentation in place

---
**Approve this plan?** Reply with modifications or "approved".
```

## Approval Workflow

1. Planner generates draft plan
2. You review and may request changes
3. You approve the final plan
4. Plan becomes your active week guide
5. Use `/start-week` to initialize templates

## Related Commands

- `/start-week` — Initialize week with approved plan
- `/status` — Check current state before planning
- `/retro` — Reflect on previous week before new plan
