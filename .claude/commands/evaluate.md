# Command: /evaluate

## Purpose

Compute progress scores based on your activity, deliverables, and learning signals. This command runs the evaluation engine and produces a detailed report for your review.

## Inputs

- **Scope**: Current month (default) or specific time range
- **Detail level**: Summary or detailed breakdown

## Outputs

1. **Evaluation Report**
   - Scores across dimensions (completion, quality, consistency, depth, reflection)
   - Overall score
   - Trend analysis (improving/declining)

2. **Signal Summary**
   - What signals were measured
   - Data sources used

3. **Recommendations**
   - Areas to focus on
   - Suggested next actions

## When to Use

- End of each week
- End of each month (before path review)
- When deciding whether to move on or remediate
- Before `/adapt-path` command

## Agent Routing

**Evaluator Agent** handles this command.

The Evaluator uses:
- `.claude/path-engine/evaluate.py`
- `.claude/memory/*` files
- `paths/Advanced/tracker.md`
- Month README for DoD criteria

## Example Usage

Basic evaluation:
```
/evaluate
```

Detailed evaluation:
```
/evaluate — Give me a detailed breakdown with all signals.
```

Specific month:
```
/evaluate — Evaluate my Month 3 progress specifically.
```

## Sample Output

```markdown
## Evaluation Report — Month 3, Week 3

### Overall Score: 7.2/10

### Dimension Scores

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Completion | 7/10 | 30% | 2.1 |
| Quality | 8/10 | 25% | 2.0 |
| Consistency | 6/10 | 20% | 1.2 |
| Depth | 7/10 | 15% | 1.05 |
| Reflection | 9/10 | 10% | 0.9 |
| **Total** | | **100%** | **7.25** |

### Dimension Details

#### Completion (7/10)
- Deliverables shipped: 3/4 (75%)
- Embedding pipeline: ✅ Complete
- Retrieval API: ✅ Complete
- Evaluation harness: 🔄 In progress (60%)
- Documentation: ⏳ Not started

#### Quality (8/10)
- Tests passing: 12/12
- Test coverage: ~65%
- DoD criteria met: 4/5
- Code review feedback: Minor issues only

#### Consistency (6/10)
- Days with progress log: 4/7
- Gap detected: Wed-Thu (2 days)
- Average session length: 1.8 hours
- Regularity could improve

#### Depth (7/10)
- Stretch goals attempted: 1/3
- Advanced topic explored: Vector quantization
- Extra learning documented: Yes

#### Reflection (9/10)
- Weekly retros: 3/3
- Best practices added: 4
- Journal entries: Complete

### Signals Used

| Signal | Source | Value |
|--------|--------|-------|
| Commits this month | Git log | 23 |
| Tests added | pytest | 8 |
| Docs updated | File changes | 5 files |
| Progress entries | progress_log.jsonl | 15 |
| Retros completed | Journal | 3 |

### Trend Analysis

```
Week 1: 6.5 ────┐
Week 2: 7.0 ────┼── Improving ↗
Week 3: 7.2 ────┘
```

### Recommendations

1. **Complete evaluation harness** — Main gap in completion score
2. **More consistent logging** — Log progress daily, even brief notes
3. **Start documentation** — Behind schedule on docs

### Path Considerations

Current trajectory suggests:
- ✅ On track to complete Month 3
- ⚠️ May need remediation week if evaluation harness slips
- Consider: Focus next week entirely on harness + docs

---

**Run `/adapt-path` for specific adaptation recommendations.**
```

## Running Programmatically

You can also run evaluation directly:

```bash
python .claude/path-engine/evaluate.py
```

This outputs JSON to stdout:

```json
{
  "overall_score": 7.25,
  "dimensions": {
    "completion": 7,
    "quality": 8,
    "consistency": 6,
    "depth": 7,
    "reflection": 9
  },
  "recommendations": [...]
}
```

## Related Commands

- `/status` — Quick status check
- `/adapt-path` — Get adaptation proposals based on evaluation
- `/retro` — Qualitative reflection alongside quantitative eval
