# Adaptation Rules

Rules governing how the learning path can be modified.

---

## Core Principle

**Human-in-the-loop**: All adaptations require explicit user approval.

```
Evaluate → Propose → User Reviews → User Approves → Apply
```

`adapt.py` outputs proposals only. It never modifies files automatically.

---

## Allowed Adaptations

The system can only propose these changes:

### 1. Level Change

Upgrade or downgrade learner level.

| Direction | Trigger | Effect |
|-----------|---------|--------|
| Upgrade | Score > 9.0 | Add higher tier content |
| Downgrade | Score < 5.0 | Reduce scope to lower tier |

**Constraints**:
- Only at month boundaries
- Preserves tier scope integrity
- Beginner ↔ Intermediate ↔ Advanced

**Schema**:
```json
{
  "type": "level_change",
  "action": "upgrade" | "downgrade",
  "from": "Intermediate",
  "to": "Advanced",
  "rationale": "Score 9.2 shows readiness for more challenge",
  "impact": "Curriculum expands to include Tier 3 content",
  "requires_approval": true
}
```

### 2. Month Reorder

Swap upcoming months within tier scope.

| Trigger | Effect |
|---------|--------|
| Dependency issues | Reorder for better flow |
| Interest alignment | Move preferred topics earlier |

**Constraints**:
- Only affects future months (not past or current)
- Must maintain tier scope
- Dependencies must still be satisfiable

**Schema**:
```json
{
  "type": "month_reorder",
  "swap": ["month-05", "month-07"],
  "rationale": "Month 7 content is prerequisite for job interview",
  "impact": "Learn Kubernetes before streaming systems",
  "requires_approval": true
}
```

### 3. Remediation Week

Insert extra time for consolidation.

| Trigger | Effect |
|---------|--------|
| Score < 6.5 | Add 1 week before next month |
| Weak dimension | Focus time on that area |

**Constraints**:
- Maximum 1 week per month
- Cannot change tier scope
- Subsequent months shift by 1 week

**Schema**:
```json
{
  "type": "remediation_week",
  "duration": "1 week",
  "focus": "consistency",
  "rationale": "Score 6.2 with weak consistency. Recommend consolidation.",
  "impact": "Month 4 starts 1 week later",
  "requires_approval": true
}
```

### 4. Project Swap

Replace month project with equivalent alternative.

| Trigger | Effect |
|---------|--------|
| Misalignment | Different project, same skills |
| Blocked by external factors | Alternative approach |

**Constraints**:
- Must be equivalent scope
- Same tier content coverage
- Similar deliverables and DoD

**Schema**:
```json
{
  "type": "project_swap",
  "current_month": 5,
  "original_project": "Time Series Forecaster",
  "proposed_project": "Demand Predictor",
  "rationale": "Better alignment with current job responsibilities",
  "impact": "Same learning goals, different domain",
  "requires_approval": true
}
```

---

## Proposal Format

All proposals follow this structure:

```json
{
  "type": "<adaptation_type>",
  "rationale": "Why this change is recommended",
  "impact": "What will happen if approved",
  "requires_approval": true
}
```

Additional fields vary by type.

---

## Approval Workflow

### Step 1: Evaluation

Run evaluation to get scores:

```
/evaluate
```

### Step 2: Get Proposals

Request adaptation proposals:

```
/adapt-path
```

### Step 3: Review

Claude presents each proposal:

```
Proposal 1: Remediation Week

Rationale: Score 6.2 with weak consistency (4/10).
Impact: Month 4 starts 1 week later.

Approve? [yes/no/modify]
```

### Step 4: Decide

For each proposal:
- **Approve**: Change will be applied
- **Reject**: No change made
- **Modify**: Adjust the proposal

### Step 5: Apply

Only approved changes are applied:
- Update memory files
- Update tracker
- Adjust curriculum pointers

---

## Thresholds

| Condition | Threshold | Proposal |
|-----------|-----------|----------|
| Level down | Score < 5.0 | Downgrade level |
| Level up | Score > 9.0 | Upgrade level |
| Remediation | Score < 6.5 | Insert 1-week remediation |

These are starting points. You can override with explicit requests.

---

## What Cannot Be Adapted

The system cannot propose:

| Change | Reason |
|--------|--------|
| Remove months | Curriculum integrity |
| Add months | Fixed 12-month structure |
| Change tier definitions | Stack is user-defined |
| Modify memory | Memory is append-only |
| Skip evaluations | Accountability |

---

## Manual Overrides

You can request changes outside the automatic proposals:

```
I'd like to swap Month 6 and Month 8. Can you create a proposal for this?
```

Claude will:
1. Validate the request fits allowed adaptations
2. Create a formal proposal
3. Show impact assessment
4. Apply only after approval

---

## Decision Logging

All approved adaptations are logged:

```json
{
  "timestamp": "2026-03-01T10:00:00Z",
  "decision": "remediation_week",
  "month": 3,
  "focus": "consistency",
  "rationale": "User approved to strengthen habits",
  "approved_by": "user"
}
```

This creates an audit trail in `decisions.jsonl`.

---

## Running adapt.py

### Via Command

```
/adapt-path
```

### Via Script

```bash
python .claude/path-engine/adapt.py
```

### With Score Override (Testing)

```bash
python .claude/path-engine/adapt.py --score 5.5
```

---

## Links

- [Rubric](rubric.md)
- [Scoring](scoring.md)
- [Signals](signals.md)
- [adapt.py](../../.claude/path-engine/adapt.py)
