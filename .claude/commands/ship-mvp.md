# Command: /ship-mvp

## Purpose

Get guidance on shipping a minimum viable product for your current project. This command helps you define the smallest useful version, prioritize features, and create a clear path to a working deliverable.

## Inputs

- **Project context**: What you're building (auto-detected from current month if not specified)
- **Current state**: What's already done
- **Time constraint**: How much time you have to ship
- **Constraints**: Any technical or scope limitations

## Outputs

1. **MVP Definition**
   - Core features (must-have)
   - Nice-to-have features (defer)
   - Out of scope (explicitly excluded)

2. **Implementation Steps**
   - Ordered task list
   - Dependencies highlighted
   - Estimated effort per step

3. **Definition of Done Checklist**
   - Minimal DoD for MVP
   - Quality bar expectations

## When to Use

- When starting a new project deliverable
- When feeling overwhelmed by scope
- When you need to ship something quickly
- Mid-project when you need to refocus on essentials

## Agent Routing

**Builder Agent** handles this command.

The Builder uses:
- Current month README for project requirements
- `.claude/skills/*.md` for relevant playbooks
- Templates in `templates/` for scaffolding

## Example Usage

Basic MVP guidance:
```
/ship-mvp
```

With time constraint:
```
/ship-mvp — I need to ship something working by Friday. I have 8 hours.
```

With specific project:
```
/ship-mvp — I'm building the embedding pipeline for RAG. What's the minimal version?
```

## Sample Output

```markdown
## MVP Definition — RAG Embedding Pipeline

### Current State
- Pinecone vector store configured
- Basic ingestion script exists
- No batching, no tests

### MVP Scope

#### Must Have (Core)
- [ ] Batch processing for documents (chunks of 100)
- [ ] Basic error handling (retry on failure)
- [ ] Single endpoint to trigger ingestion
- [ ] Logging of ingestion progress
- [ ] One integration test

#### Nice to Have (Defer to v1.1)
- Async processing queue
- Progress webhook callbacks
- Multiple embedding model support
- Comprehensive test suite

#### Out of Scope
- Real-time streaming ingestion
- Multi-tenant isolation
- Custom chunking strategies

### Implementation Steps

| Step | Task | Effort | Dependency |
|------|------|--------|------------|
| 1 | Add batching to ingestion loop | 1.5 hrs | None |
| 2 | Implement retry logic | 1 hr | Step 1 |
| 3 | Add progress logging | 30 min | Step 1 |
| 4 | Create ingestion endpoint | 1.5 hrs | Steps 1-3 |
| 5 | Write integration test | 1 hr | Step 4 |
| 6 | Update README with usage | 30 min | Step 4 |

**Total estimated**: 6 hours

### Definition of Done (MVP)

- [ ] Can ingest 1000 documents without failure
- [ ] Logs show progress and any errors
- [ ] Endpoint returns success/failure status
- [ ] One test verifies end-to-end flow
- [ ] README shows how to run

### Recommended Skills

- [api-shipping-checklist.md](../skills/api-shipping-checklist.md)
- [rag-with-evals.md](../skills/rag-with-evals.md)

---
**Ready to start?** Reply "start" to begin Step 1 implementation guidance.
```

## Builder Support

After approving the MVP scope, ask the Builder for implementation help:

```
As Builder, help me implement Step 1: Add batching to ingestion loop.
```

## Related Commands

- `/plan-week` — Integrate MVP tasks into weekly plan
- `/harden` — Polish MVP after shipping
- `/publish` — Prepare MVP for demo
