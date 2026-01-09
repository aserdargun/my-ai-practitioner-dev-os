# Command: /add-best-practice

## Purpose

Capture a learning insight or best practice that you want to remember. This command appends your insight to the living document of best practices.

## Inputs

- **The insight**: What you learned or discovered
- **Context**: When/where this applies (optional)
- **Tags**: Categories for future reference (optional)

## Outputs

1. **Draft Entry**
   - Formatted best practice entry
   - Ready for your approval

2. **Memory Update**
   - Appends to `.claude/memory/best_practices.md`
   - Only after your approval

## When to Use

- During or after a retrospective
- When you solve a tricky problem
- When you discover a useful pattern
- When you want to remember a lesson learned

## Agent Routing

**Coach Agent** handles this command.

The Coach:
- Helps you articulate the insight clearly
- Suggests formatting and categorization
- Proposes the entry for your approval

## Example Usage

Simple insight:
```
/add-best-practice — Taking 5-minute breaks every 45 minutes helps me maintain focus during long coding sessions.
```

With context:
```
/add-best-practice — When debugging embedding issues, always check the input encoding first. This would have saved me 2 hours today.
```

With tags:
```
/add-best-practice — Use pytest fixtures for vector store setup. Tags: testing, RAG, infrastructure
```

## Sample Output

```markdown
## Best Practice Capture

### Your Input
"Taking 5-minute breaks every 45 minutes helps me maintain focus during long coding sessions."

### Proposed Entry

I'll add this to `.claude/memory/best_practices.md`:

```markdown
---

### Focus Management

**Date**: 2026-03-18
**Tags**: #productivity #focus #health

**Practice**: Take 5-minute breaks every 45 minutes during long coding sessions.

**Why it works**: Prevents mental fatigue, maintains consistent productivity throughout the day, reduces context-switching costs compared to longer breaks.

**When to apply**: Any focus session longer than 45 minutes, especially deep work on complex problems.

---
```

### Approval

**Approve this entry?**
- Reply "approve" to add it
- Reply with edits to modify first
- Reply "cancel" to discard
```

## Best Practice Categories

Common categories in the document:

| Category | Description |
|----------|-------------|
| **Productivity** | Time management, focus, energy |
| **Technical** | Code patterns, debugging, architecture |
| **Learning** | Study techniques, retention, practice |
| **Tools** | IDE, CLI, libraries, workflows |
| **Communication** | Documentation, demos, writing |
| **Process** | Planning, review, shipping |

## Memory File Format

`.claude/memory/best_practices.md` structure:

```markdown
# Best Practices

Living document of learnings captured during the AI Practitioner Booster 2026 journey.

---

## Productivity

### Focus Management
...

### Time Blocking
...

---

## Technical

### Debugging Embeddings
...

### Testing RAG Systems
...

---

(entries appended chronologically within categories)
```

## Related Commands

- `/retro` — Often generates best practices
- `/debug-learning` — May surface practices to capture
- `/status` — Reference best practices when planning
