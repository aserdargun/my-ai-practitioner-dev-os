# Command: /harden

## Purpose

Review your current project and get recommendations for adding tests, documentation, and polish. This command helps you improve quality before publishing or moving on.

## Inputs

- **Project to review**: Current deliverable (auto-detected if not specified)
- **Focus areas**: Specific aspects to prioritize (tests, docs, performance, security)
- **Time budget**: How much time you can spend on hardening

## Outputs

1. **Code Review Feedback**
   - Issues found (categorized by severity)
   - Improvement suggestions
   - Security considerations

2. **Test Coverage Analysis**
   - Current coverage (if measurable)
   - Recommended tests to add
   - Test priority order

3. **Documentation Gaps**
   - Missing or incomplete docs
   - Suggested additions

4. **Improvement Checklist**
   - Prioritized action items
   - Estimated effort per item

## When to Use

- After shipping MVP, before publishing
- Before code review or PR
- At end of month before evaluation
- When preparing for demo

## Agent Routing

**Reviewer Agent** handles this command.

The Reviewer checks:
- Code quality and patterns
- Test coverage and quality
- Documentation completeness
- DoD criteria from month README

## Example Usage

Basic hardening review:
```
/harden
```

Focused on tests:
```
/harden — Focus on test coverage. I have 4 hours.
```

Security focus:
```
/harden — Review for security issues before I deploy.
```

## Sample Output

```markdown
## Hardening Review — RAG Embedding Pipeline

### Review Summary
The MVP is functional but needs hardening before demo. Priority: tests and error handling.

### Must Fix (High Priority)

1. **No input validation on document endpoint**
   - Location: `rag/ingest.py:45`
   - Risk: Malformed input could crash service
   - Fix: Add pydantic model validation
   - Effort: 30 min

2. **API key exposed in error messages**
   - Location: `rag/ingest.py:78`
   - Risk: Security issue
   - Fix: Sanitize error output
   - Effort: 15 min

### Should Fix (Medium Priority)

3. **Only one integration test**
   - Current: 1 test
   - Recommended: Add edge cases (empty doc, large doc, invalid format)
   - Effort: 1.5 hrs

4. **No docstrings on public functions**
   - Files: ingest.py, retrieve.py
   - Effort: 45 min

5. **Hardcoded batch size**
   - Location: `rag/ingest.py:23`
   - Fix: Make configurable via env var
   - Effort: 20 min

### Consider (Nice to Have)

6. **Add type hints throughout**
   - Improves maintainability
   - Effort: 1 hr

7. **Add logging levels configuration**
   - Currently all INFO
   - Effort: 30 min

### What's Working Well
- Clean separation between ingest and retrieve
- Good use of retry logic
- Clear naming conventions

### Test Recommendations

| Test | Priority | Effort |
|------|----------|--------|
| Test empty document handling | High | 20 min |
| Test batch boundary (99, 100, 101 docs) | High | 30 min |
| Test retrieval with no matches | Medium | 15 min |
| Test concurrent ingestion | Low | 45 min |

### Documentation Gaps

- [ ] Add API usage examples to README
- [ ] Document environment variables
- [ ] Add architecture diagram

### DoD Check

| Criteria | Status |
|----------|--------|
| Ingests 1000 docs without failure | ✅ Pass |
| Logs show progress | ✅ Pass |
| Endpoint returns status | ✅ Pass |
| Integration test exists | ⚠️ Minimal |
| README shows usage | ⚠️ Needs examples |

---
**Recommended next action**: Fix items 1-2 (security), then add tests (item 3).
```

## Related Commands

- `/ship-mvp` — Ship first, then harden
- `/publish` — After hardening, publish
- `/evaluate` — Check overall progress after hardening
