# How to Demo

Guide for demonstrating your projects effectively.

---

## Overview

A good demo:
- Shows your project working
- Explains what problem it solves
- Highlights technical decisions
- Fits in 5-10 minutes

---

## Demo Structure

### 1. Opening (30 seconds)

State what you built and why it matters.

```
"I built a production-ready RAG pipeline that enables semantic search
over 1000+ documents. Let me show you how it works."
```

### 2. The Problem (1 minute)

Explain the problem you solved.

```
"Traditional keyword search fails when users ask questions in natural
language. We needed a way to find answers based on meaning, not just
matching words."
```

### 3. Live Demo (3-4 minutes)

Show the system working. Key tips:

- **Prepare your environment** beforehand
- **Have sample inputs** ready
- **Show the happy path** first
- **Show one edge case** to demonstrate robustness
- **Talk while demonstrating**

Example flow:
1. Show the input (documents, query)
2. Run the system
3. Show the output
4. Explain what happened

### 4. Technical Deep Dive (2 minutes)

Explain key technical decisions.

```
"I chose to use 512-token chunks with 50-token overlap because...
The embedding model is BGE-base because our experiments showed..."
```

Show:
- Architecture diagram (if helpful)
- Key code snippet
- Metrics/evaluation results

### 5. Learnings (1 minute)

Share what you learned.

```
"The biggest challenge was chunking strategy. I learned that
chunk boundaries matter more than chunk size for retrieval quality."
```

### 6. Close (30 seconds)

Wrap up with next steps or links.

```
"The code is on GitHub. I'm planning to add reranking next.
Questions?"
```

---

## Demo Checklist

### Before the Demo

- [ ] System is running and tested
- [ ] Sample inputs prepared
- [ ] Environment variables set
- [ ] Screen sharing works
- [ ] Backup plan if live demo fails

### During the Demo

- [ ] Speak clearly and at moderate pace
- [ ] Explain what you're doing
- [ ] Pause for questions if applicable
- [ ] Don't apologize for simplicity

### After the Demo

- [ ] Share links (repo, blog post)
- [ ] Answer questions
- [ ] Note feedback for improvement

---

## Demo Formats

### Live Demo

Show the system running in real-time.

**Pros**: Authentic, shows real performance
**Cons**: Things can break

**Tips**:
- Test everything beforehand
- Have a backup (screenshots, video)
- Prepare recovery if things fail

### Recorded Demo

Pre-recorded video of the system.

**Pros**: No live failures, can edit
**Cons**: Less engaging, can't adapt

**Tips**:
- Keep it under 5 minutes
- Add voiceover or captions
- Include intro and outro

### Walkthrough

Code walkthrough with explanations.

**Pros**: Good for technical audience
**Cons**: Less exciting

**Tips**:
- Focus on interesting decisions
- Skip boilerplate
- Use comments/highlights

---

## Demo for Different Audiences

### Technical Peers

- More architecture details
- Show code snippets
- Discuss trade-offs
- Accept technical questions

### Hiring Managers

- Focus on problem-solving
- Highlight impact
- Show completeness
- Demonstrate communication skills

### General Audience

- Keep it high-level
- Avoid jargon
- Focus on the "what" and "why"
- Make it relatable

---

## Common Demo Mistakes

### Talking Too Fast

Slow down. Pause between sections.

### Showing Everything

Focus on highlights. You can share the repo for details.

### Apologizing

"This is just a simple project..." — Don't diminish your work.

### No Story

Frame it as a journey: problem → solution → result.

### Technical Failures

Always have a backup. Screenshots, video, or slides.

---

## Demo Script Template

```markdown
# Demo: [Project Name]

## Opening
[One sentence on what it is and why it matters]

## The Problem
[2-3 sentences on the problem]

## Demo Steps
1. [Step 1 - what to show, what to say]
2. [Step 2]
3. [Step 3]
4. [Edge case]

## Technical Highlights
- [Decision 1 and why]
- [Decision 2 and why]
- [Key metric]

## Learnings
- [Main lesson]

## Close
- [Next steps]
- [Links]
```

---

## Recording Tips

If recording your demo:

1. **Clean desktop** — Hide personal items
2. **Large font** — At least 16pt in terminal
3. **Good audio** — Use a microphone
4. **Quiet environment** — Minimize background noise
5. **Record in segments** — Edit together later
6. **Keep it short** — 3-5 minutes ideal

---

## Links

- [Portfolio checklist](portfolio-checklist.md)
- [How to write Medium post](how-to-write-medium-post.md)
- [/publish command](../../.claude/commands/publish.md)
