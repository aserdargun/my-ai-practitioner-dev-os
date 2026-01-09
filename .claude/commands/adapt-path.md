# Command: /adapt-path

## Purpose

Get path change recommendations based on your evaluation results. This command proposes adaptations to your learning path—but all changes require your explicit approval.

## Inputs

- **Evaluation results**: From recent `/evaluate` run
- **Preferences**: Any constraints on adaptations you'd accept

## Outputs

1. **Adaptation Proposals**
   - Specific changes recommended
   - Rationale for each
   - Impact assessment

2. **Approval Request**
   - Clear yes/no decision points
   - What happens if approved/rejected

## When to Use

- End of each month
- After evaluation shows significant gaps
- When feeling overwhelmed or underwhelmed
- At natural transition points

## Agent Routing

**Evaluator Agent** handles this command.

The Evaluator uses:
- `.claude/path-engine/adapt.py`
- Recent evaluation scores
- `docs/evaluation/adaptation-rules.md` for allowed mutations

## Allowed Adaptations

The system can ONLY propose these changes:

| Adaptation | Description |
|------------|-------------|
| **Level change** | Upgrade/downgrade (Beginner ↔ Intermediate ↔ Advanced) |
| **Month reorder** | Swap upcoming months within tier scope |
| **Remediation week** | Insert 1-week remediation inside a month |
| **Project swap** | Replace project with equivalent scope alternative |

**Critical**: No adaptations are applied automatically. You must explicitly approve each change.

## Example Usage

Basic adaptation check:
```
/adapt-path
```

With constraints:
```
/adapt-path — I don't want to change my level. Only suggest within-month adjustments.
```

After evaluation:
```
/adapt-path — Based on my 6.5 score, what do you recommend?
```

## Sample Output

```markdown
## Path Adaptation Proposals — Month 3 Review

### Current State
- **Level**: Advanced
- **Month**: 3 (RAG Systems)
- **Evaluation Score**: 6.5/10
- **Key Gap**: Evaluation harness incomplete, documentation behind

### Proposal 1: Remediation Week

**Recommendation**: Insert 1-week remediation block before Month 4

**Rationale**:
- Evaluation harness is critical for Month 4 (which builds on RAG evals)
- Documentation debt will compound if not addressed
- One extra week prevents rushing and reduces frustration

**Impact**:
- Month 4 starts 1 week later
- Months 5-12 shift by 1 week (still completes in 2026)
- Quality of foundation improves

**Approval Required**:
```
[ ] Approve remediation week
[ ] Reject — proceed to Month 4 as scheduled
```

### Proposal 2: Project Scope Reduction

**Recommendation**: Reduce Month 3 evaluation harness scope

**Rationale**:
- Current scope may be too ambitious for remaining time
- Can defer advanced grading features to Month 4

**Impact**:
- Ship minimal harness this week
- Add advanced features as stretch goal in Month 4
- Better completion score

**Approval Required**:
```
[ ] Approve scope reduction
[ ] Reject — maintain original scope
```

### NOT Proposed (and why)

- **Level change**: Score 6.5 is challenging but not failing (threshold: 5.0)
- **Month reorder**: Month 3→4 dependency makes reorder inadvisable
- **Project swap**: No equivalent alternative available for RAG evaluations

### Decision Summary

Please review and respond with your decisions:

```
Proposal 1 (Remediation Week): [approve/reject]
Proposal 2 (Scope Reduction): [approve/reject]
```

---

**Note**: If you approve any changes, I'll update the tracker and memory files (after showing you the exact changes).
```

## Approval Workflow

1. `/evaluate` generates scores
2. `/adapt-path` proposes changes
3. You review each proposal
4. You explicitly approve or reject
5. Only approved changes are applied
6. Changes are logged to `.claude/memory/decisions.jsonl`

## Running Programmatically

```bash
python .claude/path-engine/adapt.py
```

Outputs JSON proposals:

```json
{
  "proposals": [
    {
      "type": "remediation_week",
      "rationale": "...",
      "impact": "...",
      "requires_approval": true
    }
  ]
}
```

## Related Commands

- `/evaluate` — Run before adapt-path
- `/status` — Check current state
- `/plan-week` — Plan after adaptations approved
