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

*(Add tool and workflow tips here)*

---
