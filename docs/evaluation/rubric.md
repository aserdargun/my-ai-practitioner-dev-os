# Evaluation Rubric

Scoring framework for the AI Practitioner Booster 2026 learning system.

---

## Overview

Progress is evaluated across five dimensions:

| Dimension | Weight | Focus |
|-----------|--------|-------|
| Completion | 30% | Shipping deliverables |
| Quality | 25% | Meeting Definition of Done |
| Consistency | 20% | Regular progress |
| Depth | 15% | Going beyond basics |
| Reflection | 10% | Learning from experience |

Overall score = weighted average of dimension scores.

---

## Dimension Rubrics

### Completion (30%)

How well are you shipping deliverables?

| Score | Description |
|-------|-------------|
| 10 | All deliverables shipped ahead of schedule |
| 8-9 | All deliverables shipped on time |
| 6-7 | Most deliverables shipped, minor gaps |
| 4-5 | Some deliverables shipped, significant gaps |
| 2-3 | Few deliverables shipped |
| 0-1 | No progress on deliverables |

**Signals measured**:
- Deliverables shipped vs. planned
- Week completion status
- Month milestones hit

### Quality (25%)

Are deliverables meeting the quality bar?

| Score | Description |
|-------|-------------|
| 10 | Exceeds DoD, well-tested, documented |
| 8-9 | Meets DoD, good test coverage |
| 6-7 | Mostly meets DoD, some gaps |
| 4-5 | Partially meets DoD, significant issues |
| 2-3 | Major quality issues |
| 0-1 | Deliverables don't meet basic criteria |

**Signals measured**:
- Definition of Done checklist completion
- Test suite status
- Code review feedback
- Documentation completeness

### Consistency (20%)

Are you making regular progress?

| Score | Description |
|-------|-------------|
| 10 | Daily progress logged, regular rhythm |
| 8-9 | Most days have progress, good consistency |
| 6-7 | Regular but with gaps |
| 4-5 | Sporadic progress |
| 2-3 | Very inconsistent |
| 0-1 | Long periods without progress |

**Signals measured**:
- Days with progress log entries
- Gaps between entries
- Session length patterns

### Depth (15%)

Are you going beyond the basics?

| Score | Description |
|-------|-------------|
| 10 | Multiple stretch goals, deep exploration |
| 8-9 | Stretch goals attempted, good depth |
| 6-7 | Some exploration beyond requirements |
| 4-5 | Basics covered, minimal exploration |
| 2-3 | Bare minimum only |
| 0-1 | Not meeting basic requirements |

**Signals measured**:
- Stretch goals attempted
- Research documented
- Extra learning recorded

### Reflection (10%)

Are you learning from experience?

| Score | Description |
|-------|-------------|
| 10 | Regular retros, many best practices captured |
| 8-9 | Weekly retros, good practice capture |
| 6-7 | Some reflection, occasional captures |
| 4-5 | Minimal reflection |
| 2-3 | Rare reflection |
| 0-1 | No reflection activities |

**Signals measured**:
- Retrospectives completed
- Best practices added
- Journal entries made

---

## Overall Score Interpretation

| Score | Status | Recommendation |
|-------|--------|----------------|
| 9.0+ | Excellent | Consider level upgrade |
| 7.5-8.9 | Strong | On track, keep momentum |
| 6.5-7.4 | Good | Minor adjustments may help |
| 5.0-6.4 | Needs attention | Consider remediation |
| < 5.0 | At risk | Level downgrade may help |

---

## Thresholds

These thresholds trigger adaptation proposals:

| Condition | Threshold | Proposal |
|-----------|-----------|----------|
| Level upgrade | > 9.0 | Upgrade to next level |
| Level downgrade | < 5.0 | Downgrade to easier level |
| Remediation | < 6.5 | Insert remediation week |
| Acceleration | > 9.5 | Skip or compress content |

---

## Running Evaluation

### Via Command

```
/evaluate
```

### Via Script

```bash
python .claude/path-engine/evaluate.py
```

### Output Format

```json
{
  "overall_score": 7.5,
  "dimensions": {
    "completion": 7,
    "quality": 8,
    "consistency": 6,
    "depth": 8,
    "reflection": 9
  },
  "recommendations": [...]
}
```

---

## Tips for Better Scores

### Completion

- Ship early and iterate
- Use `/ship-mvp` to focus on essentials
- Break work into smaller deliverables

### Quality

- Check DoD before marking complete
- Write tests as you go
- Get feedback with `/harden`

### Consistency

- Log progress daily, even brief notes
- Set regular learning times
- Use `/start-week` to establish rhythm

### Depth

- Attempt at least one stretch goal per month
- Document what you learn beyond requirements
- Explore related topics

### Reflection

- Run `/retro` weekly
- Capture best practices immediately
- Keep journal entries current

---

## Links

- [Scoring details](scoring.md)
- [Signal sources](signals.md)
- [Adaptation rules](adaptation-rules.md)
- [Path engine](../../.claude/path-engine/)
