# Command: /retro

## Purpose

Run a weekly retrospective to reflect on what worked, what didn't, and what to try next. This command facilitates structured reflection to improve your learning process.

## Inputs

- **Week context**: Auto-detected from current date
- **Focus areas**: Specific aspects to reflect on (optional)

## Outputs

1. **Retrospective Summary**
   - What went well
   - What could be improved
   - Action items for next week

2. **Journal Update**
   - Retrospective section filled in week's journal entry

3. **Progress Log Entry**
   - Retro completion logged (with your approval)

## When to Use

- Every Friday (or your week end day)
- End of each month
- After completing a major deliverable
- When feeling stuck or frustrated

## Agent Routing

**Coach Agent** handles this command.

The Coach:
- Facilitates reflection using structured prompts
- Helps identify patterns across weeks
- Suggests strategies based on your reflections

## Example Usage

Basic retro:
```
/retro
```

Focused retro:
```
/retro — Focus on time management this week.
```

Monthly retro:
```
/retro — This is end of month. Let's do a deeper reflection.
```

## Sample Output

```markdown
## Weekly Retrospective — Week 11 (March 15-21, 2026)

### Reflection Prompts

I'll ask you a few questions. Take a moment to think before answering.

1. **What went well this week?**
   - What accomplishments are you proud of?
   - What felt easy or enjoyable?
   - What skills did you apply effectively?

2. **What was challenging?**
   - Where did you struggle?
   - What took longer than expected?
   - What felt frustrating?

3. **What did you learn?**
   - New technical knowledge?
   - About your learning process?
   - About the tools/technologies?

4. **What will you try differently next week?**
   - Specific changes to your approach?
   - Experiments to run?
   - Habits to adjust?

---

### Your Responses

*(After you answer, I'll summarize)*

---

### Retrospective Summary

#### What Went Well
- Completed embedding pipeline ahead of schedule
- Batch optimization was cleaner than expected
- Good momentum on Tuesday and Thursday sessions

#### What Could Be Improved
- Wednesday off disrupted flow; hard to restart Thursday
- Underestimated documentation time
- Got distracted by Slack during focus time

#### Patterns Noticed
- You work better in 2-hour blocks than 30-minute sprints
- Morning sessions more productive than evening
- Pair programming with Claude helps overcome blocks faster

#### Action Items for Next Week
1. [ ] Block 2-hour morning sessions (not 30-min chunks)
2. [ ] Turn off Slack during focus time
3. [ ] Schedule documentation as separate task, not afterthought

### Best Practice Candidate

Based on this retro, consider capturing:

> "2-hour morning focus blocks are more effective than fragmented 30-minute sessions. Protect these blocks from meetings and notifications."

**Want me to add this to best_practices.md?**

---

### Memory Update (Pending Approval)

```json
{
  "timestamp": "2026-03-21T17:00:00Z",
  "event": "retro_complete",
  "week": 11,
  "highlights": ["embedding_pipeline_complete", "batch_optimization"],
  "challenges": ["context_switching", "documentation_underestimated"],
  "action_items": ["2hr_blocks", "focus_mode", "schedule_docs"]
}
```

**Approve this progress log entry?**
```

## Retrospective Formats

### Weekly (15-20 min)
Quick check-in on the week. Good for maintaining momentum.

### Monthly (30-45 min)
Deeper reflection on month's goals, deliverables, and growth.

### Quarterly (1 hr)
Big-picture review of trajectory, skill development, and path adjustments.

## Related Commands

- `/add-best-practice` — Capture insights from retro
- `/plan-week` — Apply learnings to next week
- `/evaluate` — See quantitative progress alongside qualitative retro
- `/debug-learning` — If retro reveals blockers
