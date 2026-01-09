# Command: /status

## Purpose

View your current learning progress, active blockers, and suggested next actions. This is your quick health check on where you stand in your learning journey.

## Inputs

No inputs required. The command reads from your memory files and tracker automatically.

Optional context you can add:
- Specific area to focus on (e.g., "for Month 3")
- Whether you want a detailed or summary view

## Outputs

1. **Progress Summary**
   - Current month and week
   - Completion percentage for current month
   - Key deliverables status (done/in-progress/pending)

2. **Blockers**
   - Active blockers from progress log
   - Suggested resolutions

3. **Next Actions**
   - Top 3 recommended next steps
   - Priority ranking

## When to Use

- Start of each day to orient yourself
- When returning after a break
- When you feel lost or unsure what to do next
- Before planning sessions
- After completing a significant deliverable

## Agent Routing

**Evaluator Agent** handles this command.

The Evaluator reads from:
- `.claude/memory/progress_log.jsonl`
- `.claude/memory/learner_profile.json`
- `paths/Advanced/tracker.md`
- Current month's README

## Example Usage

Basic status check:
```
/status
```

Detailed status for specific month:
```
/status — Give me a detailed breakdown for Month 5 progress.
```

Focus on blockers:
```
/status — What's blocking my progress right now?
```

## Sample Output

```markdown
## Status Report — 2026-03-15

### Current Position
- **Month**: 3 of 12 (RAG Systems)
- **Week**: 2 of 4
- **Overall Progress**: 42% complete

### Deliverables
| Deliverable | Status | Notes |
|-------------|--------|-------|
| Vector store setup | ✅ Done | Pinecone integrated |
| Embedding pipeline | 🔄 In Progress | 70% complete |
| Retrieval API | ⏳ Pending | Blocked by pipeline |
| Evaluation harness | ⏳ Pending | Week 3 |

### Blockers
1. **Embedding pipeline performance** — Batching not optimized
   - Suggested: Review chunking strategy, consider async processing

### Recommended Next Actions
1. Complete embedding pipeline batch optimization
2. Write tests for current retrieval logic
3. Document API contract for retrieval endpoint
```

## Related Commands

- `/plan-week` — Create a plan based on status
- `/evaluate` — Get detailed scores
- `/debug-learning` — Diagnose blockers
