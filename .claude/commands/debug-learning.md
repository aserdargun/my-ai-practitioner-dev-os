# Command: /debug-learning

## Purpose

Troubleshoot learning blocks and get strategies to overcome them. This command helps diagnose why you're stuck and provides actionable solutions.

## Inputs

- **Description of the block**: What you're struggling with
- **Context**: How long you've been stuck, what you've tried
- **Symptoms**: Frustration, confusion, avoidance, etc.

## Outputs

1. **Diagnosis**
   - Type of block identified
   - Root cause analysis

2. **Strategies**
   - Specific actions to try
   - Resources that might help

3. **Reframe**
   - Perspective shift if helpful
   - Reminder of progress made

## When to Use

- When stuck on a concept for more than a day
- When procrastinating on specific tasks
- When feeling frustrated or overwhelmed
- When motivation is low

## Agent Routing

**Coach Agent** handles this command.

The Coach uses:
- Blocker categories framework
- Your learner profile and history
- Best practices that have worked before

## Blocker Categories

| Type | Description | Common Solutions |
|------|-------------|------------------|
| **Knowledge gap** | Missing prerequisite | Find and study prerequisites |
| **Skill gap** | Know theory, need practice | Hands-on exercises, repetition |
| **Motivation** | Energy or interest issues | Connect to goals, smaller chunks |
| **Environment** | Tools, time, setup | Fix environment first |
| **Clarity** | Unclear requirements | Clarify before continuing |
| **Perfectionism** | Fear of doing it wrong | Ship ugly first version |
| **Overwhelm** | Too much at once | Break into smaller pieces |

## Example Usage

Concept block:
```
/debug-learning — I've been stuck on understanding attention mechanisms for 3 days.
```

Motivation block:
```
/debug-learning — I keep procrastinating on the Kubernetes section. I know it's important but I can't start.
```

Confusion block:
```
/debug-learning — The RAG evaluation metrics are confusing. I don't know which ones matter.
```

## Sample Output

```markdown
## Learning Block Diagnosis

### Your Block
"I've been stuck on understanding attention mechanisms for 3 days."

### Diagnosis

**Block Type**: Knowledge Gap + Overwhelm

**Root Cause Analysis**:
1. Attention mechanisms have multiple components (Q, K, V, multi-head, etc.)
2. Many explanations assume linear algebra background
3. Jumping to transformer architecture before understanding single attention

**Contributing Factors**:
- Trying to understand everything at once
- Reading papers instead of implementing
- No intermediate checkpoints to validate understanding

### Recommended Strategies

#### Strategy 1: Foundation First (2 hours)
Before attention, ensure you're solid on:
- [ ] Matrix multiplication intuition
- [ ] Dot product as similarity measure
- [ ] Softmax function behavior

**Resource**: [3Blue1Brown: Linear Algebra Essence](link) (watch chapters 1-4)

#### Strategy 2: Build One Piece at a Time (3 hours)
Implement attention step-by-step:
1. [ ] Single query-key-value computation (30 min)
2. [ ] Scaled dot-product (20 min)
3. [ ] Softmax weighting (20 min)
4. [ ] Value aggregation (20 min)
5. [ ] Multi-head extension (1 hr)
6. [ ] Self-attention (30 min)

**Resource**: [The Illustrated Transformer](link) — follow along with code

#### Strategy 3: Verbal Explanation Test
After each step, explain in your own words:
- What is this step doing?
- Why is it necessary?
- What would break if we removed it?

If you can't explain it, you don't understand it yet. That's the signal to dig deeper.

### Reframe

You're learning one of the most important innovations in modern ML. It's supposed to be hard. Three days of struggle is normal—many people take weeks.

**Progress reminder**:
- You've already implemented RNN and LSTM (these are prerequisites!)
- You've built embedding pipelines (related concept)
- You're closer than you think

### Suggested Next Action

Start with Strategy 1: Spend 1 hour on matrix multiplication visualization. Then come back and try implementing single attention from scratch.

---

**Would you like me to create a mini-plan for tackling attention mechanisms this week?**
```

## Follow-Up Actions

After debugging:

```
/plan-week — Include the strategies from debug-learning for tackling attention mechanisms.
```

Or capture the learning:

```
/add-best-practice — When stuck on complex concepts, implement the simplest version first before reading more theory.
```

## Related Commands

- `/status` — Check if block is reflected in status
- `/plan-week` — Incorporate unblocking strategies
- `/retro` — Reflect on what caused the block
- `/add-best-practice` — Capture what worked
