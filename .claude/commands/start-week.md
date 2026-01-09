# Command: /start-week

## Purpose

Initialize a new week with templates and scaffolding. This command creates the week's journal entry, updates the tracker, and prepares your workspace for the week ahead.

## Inputs

- **Week plan**: The approved plan from `/plan-week`
- Optional: Any adjustments to the plan

## Outputs

1. **Week Journal Entry**
   - New entry in `paths/Advanced/journal/` based on weekly template
   - Pre-filled with planned tasks

2. **Tracker Update**
   - `paths/Advanced/tracker.md` updated with new week pointer
   - Progress log entry for week start

3. **Hook Execution** (optional)
   - Runs `pre_week_start.sh` if approved

## When to Use

- After approving your `/plan-week` output
- Every Monday (or your week start day)
- When starting a new month

## Agent Routing

**Planner Agent** handles this command.

The Planner:
- Creates journal entry from template
- Updates tracker
- Proposes memory updates (with your approval)

## Example Usage

Basic start:
```
/start-week
```

With plan reference:
```
/start-week — Use the plan I just approved focusing on the RAG evaluation harness.
```

With adjustments:
```
/start-week — Same plan but swap Thursday and Friday tasks.
```

## Sample Output

```markdown
## Week Initialization — Week of March 15, 2026

### Created Files

1. **Journal Entry**: `paths/Advanced/journal/2026-w11.md`

   ```markdown
   # Week 11 — March 15-21, 2026

   ## Goals
   - Complete embedding pipeline with tests
   - Start retrieval API
   - Document API contract

   ## Daily Log

   ### Monday
   - [ ] Review embedding pipeline code
   - [ ] Implement batch optimization
   - [ ] Write batch processing tests

   ### Tuesday
   - [ ] Complete embedding pipeline
   - [ ] Start retrieval API scaffold

   ... (rest of week)

   ## Reflections
   (To be filled during /retro)
   ```

2. **Tracker Updated**: `paths/Advanced/tracker.md`
   - Current week pointer: Week 11
   - Month 3 progress: 45%

### Memory Updates (Pending Approval)

The following will be appended to `.claude/memory/progress_log.jsonl`:

```json
{
  "timestamp": "2026-03-15T09:00:00Z",
  "event": "week_start",
  "week": 11,
  "month": 3,
  "planned_hours": 12,
  "focus": ["embedding_pipeline", "retrieval_api"]
}
```

**Approve these changes?**
```

## Approval Workflow

1. Review created files
2. Review proposed memory updates
3. Approve or request modifications
4. Changes are applied
5. Optionally run `pre_week_start.sh` hook

## Hook Integration

If you approve, the command can run:

```bash
bash .claude/hooks/pre_week_start.sh
```

This hook:
- Validates plan exists
- Creates week directory if needed
- Updates tracker programmatically

## Related Commands

- `/plan-week` — Create the plan first
- `/status` — Check current state
- `/retro` — Run at end of week
