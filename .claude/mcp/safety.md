# MCP Safety Guidelines

Security, privacy, and evaluation integrity rules for MCP tools in the AI Practitioner Booster 2026 system.

---

## Core Principles

### 1. Minimal Access

Tools have only the permissions necessary for their function:

- `hello`: No file access
- `read_repo_file`: Read-only, filtered paths
- `write_memory_entry`: Append-only, memory files only

### 2. Append-Only Memory

Memory files cannot be overwritten or deleted:

- Preserves full learning history
- Enables audit and analysis
- Prevents accidental data loss

### 3. User Approval

Sensitive operations require explicit confirmation:

- All write operations
- Any action that modifies learning path
- External service calls (if added)

### 4. Audit Trail

All tool calls are logged:

- Timestamp
- Tool name
- Parameters (sanitized)
- Result status
- User context

---

## Secrets and Sensitive Data

### Never Expose

The following are blocked from all read operations:

| Pattern | Reason |
|---------|--------|
| `.env*` | Environment variables |
| `*.key` | Private keys |
| `*.pem` | Certificates |
| `**/secrets/**` | Secrets directory |
| `**/credentials*` | Credential files |
| `**/*password*` | Password files |
| `**/*token*` | Token files |

### Never Log

Tool implementations must never log:

- API keys
- Passwords
- Tokens
- Personal identifiers
- Full file contents (use truncated previews)

### Sanitization

Parameters are sanitized before logging:

```python
def sanitize_params(params):
    sensitive_keys = ['password', 'token', 'key', 'secret']
    sanitized = params.copy()
    for key in sensitive_keys:
        if key in sanitized:
            sanitized[key] = '[REDACTED]'
    return sanitized
```

---

## Privacy Guidelines

### Personal Data

- Learner profile data stays local
- No automatic upload of learning data
- User controls what to share

### Memory Contents

- Progress logs may contain personal notes
- Best practices may reveal learning style
- Handle as confidential

### Sharing

If sharing features are added:

- Require explicit opt-in
- Show exactly what will be shared
- Allow granular selection

---

## Evaluation Integrity

### Score Manipulation Prevention

Tools cannot:

- Directly modify evaluation scores
- Bypass evaluation logic
- Forge progress events

### Honest Logging

Progress events must be:

- Timestamped accurately
- Reflect actual completion
- Created through normal workflow

### Audit Capability

The system maintains ability to:

- Reconstruct evaluation history
- Verify progress claims
- Detect anomalies

---

## Tool-Specific Rules

### read_repo_file

```yaml
Allowed:
  - paths/**/*
  - .claude/**/*  (except secrets)
  - docs/**/*
  - templates/**/*
  - examples/**/*
  - stacks/**/*
  - README.md
  - CLAUDE.md
  - SETUP.md

Blocked:
  - .env*
  - *.key
  - *.pem
  - **/secrets/**
  - **/.git/**
  - **/node_modules/**
  - **/__pycache__/**

Limits:
  - Max file size: 1MB
  - Rate: 100/minute
```

### write_memory_entry

```yaml
Allowed Files:
  - progress_log.jsonl
  - decisions.jsonl
  - best_practices.md

Constraints:
  - Append-only (no overwrite)
  - Max entry size: 10KB
  - User approval required
  - Timestamp validated

Validation:
  - JSON lines must be valid JSON
  - Markdown must not contain scripts
  - Content must not be empty
```

---

## Error Handling

### Safe Defaults

On error, tools should:

- Return generic error message
- Not leak file paths or structure
- Not reveal internal state
- Log details server-side only

### Example

```python
# Bad: Exposes internal details
raise Exception(f"Failed to read {full_path}: {internal_error}")

# Good: Safe error message
raise MCPError(404, "File not found")
```

---

## Implementation Checklist

### For Tool Developers

- [ ] Validate all inputs
- [ ] Check path patterns before access
- [ ] Enforce size limits
- [ ] Require approval for writes
- [ ] Log sanitized requests
- [ ] Return safe error messages
- [ ] Test with malicious inputs

### For Server Operators

- [ ] Run with minimal permissions
- [ ] Use HTTPS in production
- [ ] Rotate any API keys
- [ ] Monitor for anomalies
- [ ] Keep audit logs
- [ ] Regular security review

---

## Incident Response

If security issue is discovered:

1. **Contain**: Disable affected tool
2. **Assess**: Determine scope
3. **Notify**: Inform affected users
4. **Fix**: Patch vulnerability
5. **Learn**: Update guidelines

---

## Updates

This document should be reviewed when:

- Adding new tools
- Changing tool permissions
- After security incidents
- Quarterly (minimum)

Last reviewed: 2026-01-09
