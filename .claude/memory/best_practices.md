# Best Practices

Living document of learnings captured during the AI Practitioner Booster 2026 journey.

This file is append-only. Add new entries at the bottom with a date header.

---

## Getting Started

### 2026-01-09 — Initial Setup

Welcome to your learning journey! This file will grow as you discover what works for you.

**How to add entries:**
- Use the `/add-best-practice` command to capture insights
- Or manually add entries following the format below
- Include the date and a descriptive title
- Explain what you learned and why it matters

**Entry format:**
```markdown
## YYYY-MM-DD — Title

Description of the practice or insight.

Why it works or when to apply it.
```

---

## Productivity

*(Add productivity insights here)*

---

## Technical

### 2026-01-10 — Comprehensive Testing Strategy

Every module should have tests covering:
- Happy path (normal usage)
- Edge cases (empty inputs, special characters)
- Error conditions (invalid parameters)
- Integration with other components

114 tests for 8 modules = ~14 tests per module average. This provides confidence when refactoring.

### 2026-01-10 — Docstrings for All Functions

All functions should have docstrings explaining:
- Purpose (what it does)
- Args (parameters and types)
- Returns (what it gives back)
- Raises (exceptions if any)

This enables IDE autocomplete and serves as inline documentation.

### 2026-01-10 — Test Edge Cases Early

Add tests for edge cases (zero vectors, empty inputs, malformed data) early in development, not just happy-path tests.

**Why it works:** The zero-vector similarity bug would have caused division-by-zero in production. Edge case tests caught it and improved coverage from 93% to 98%.

**When to apply:** Any numeric computation, especially similarity/distance functions.

### 2026-01-10 — Use sklearn-Style API for ML Components

Implement `fit()`, `transform()`, `fit_transform()`, and method chaining for any ML pipeline component.

**Why it works:** Familiar API reduces cognitive load. Method chaining enables clean one-liners: `Pipeline().fit(X).transform(new_X)`. Easy to swap components.

**When to apply:** Any data transformation or ML pipeline component.

### 2026-01-10 — Target 90%+ Coverage, Not 100%

Aim for 90%+ coverage. The last 5-10% often covers rare edge cases (file I/O errors, network timeouts) that require complex mocking for little value.

**Why it works:** 98% coverage with 117 tests provides high confidence. Remaining 2% is NLTK download paths and binary file edge cases—low-risk code.

**When to apply:** Test strategy for any project. Focus effort on business logic.

---

## Learning Strategies

### 2026-01-10 — Observe-Then-Implement Learning

When learning new concepts, observing code being built first and then trying similar patterns yourself is effective. This approach:
- Reduces cognitive load by separating "understanding" from "doing"
- Allows you to see the full picture before diving into details
- Makes it easier to ask targeted questions during implementation

**When to apply:** New algorithms, unfamiliar libraries, complex system designs.

---

## Tools & Workflows

### 2026-01-10 — Run Linter Before Committing

Run `ruff check --fix` before every commit. Configure as pre-commit hook.

**Why it works:** Caught 11 issues (unused imports, ambiguous variable names, import sorting) that would have accumulated as tech debt. Auto-fix handles 80%+ of issues.

**When to apply:** Every Python project from day one.

---
