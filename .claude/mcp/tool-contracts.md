# Tool Contracts

Formal specifications for MCP tools available in the AI Practitioner Booster 2026 learning system.

---

## hello

Test tool to verify MCP connectivity.

### Schema

```json
{
  "name": "hello",
  "description": "Returns a greeting message. Use for testing MCP connectivity.",
  "parameters": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string",
        "description": "Name to greet",
        "default": "World"
      }
    },
    "required": []
  },
  "returns": {
    "type": "object",
    "properties": {
      "message": {
        "type": "string",
        "description": "Greeting message"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time",
        "description": "Server timestamp"
      }
    }
  }
}
```

### Example

**Request:**
```json
{
  "tool": "hello",
  "parameters": {
    "name": "Learner"
  }
}
```

**Response:**
```json
{
  "message": "Hello, Learner!",
  "timestamp": "2026-01-09T10:30:00Z"
}
```

### Constraints

- No authentication required
- Rate limit: 100 requests/minute
- Safe: No side effects

---

## read_repo_file

Read a file from the repository.

### Schema

```json
{
  "name": "read_repo_file",
  "description": "Read a file from the repository. Limited to safe paths.",
  "parameters": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "description": "Relative path from repo root",
        "pattern": "^[a-zA-Z0-9_./-]+$"
      },
      "encoding": {
        "type": "string",
        "enum": ["utf-8", "base64"],
        "default": "utf-8"
      }
    },
    "required": ["path"]
  },
  "returns": {
    "type": "object",
    "properties": {
      "content": {
        "type": "string",
        "description": "File content"
      },
      "size": {
        "type": "integer",
        "description": "File size in bytes"
      },
      "modified": {
        "type": "string",
        "format": "date-time",
        "description": "Last modified timestamp"
      }
    }
  }
}
```

### Example

**Request:**
```json
{
  "tool": "read_repo_file",
  "parameters": {
    "path": "paths/Advanced/tracker.md"
  }
}
```

**Response:**
```json
{
  "content": "# Progress Tracker\n\n...",
  "size": 1234,
  "modified": "2026-01-09T10:00:00Z"
}
```

### Constraints

- **Allowed paths**: Files in repo root only
- **Blocked paths**:
  - `.env*` files
  - `**/secrets/**`
  - `**/*.key`
  - `**/*.pem`
- **Max file size**: 1MB
- **Read-only**: Cannot modify files

---

## write_memory_entry

Append an entry to a memory file.

### Schema

```json
{
  "name": "write_memory_entry",
  "description": "Append an entry to a memory file. Only supports append operations.",
  "parameters": {
    "type": "object",
    "properties": {
      "file": {
        "type": "string",
        "enum": ["progress_log.jsonl", "decisions.jsonl", "best_practices.md"],
        "description": "Target memory file"
      },
      "entry": {
        "type": "string",
        "description": "Content to append"
      }
    },
    "required": ["file", "entry"]
  },
  "returns": {
    "type": "object",
    "properties": {
      "success": {
        "type": "boolean"
      },
      "bytes_written": {
        "type": "integer"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time"
      }
    }
  }
}
```

### Example

**Request:**
```json
{
  "tool": "write_memory_entry",
  "parameters": {
    "file": "progress_log.jsonl",
    "entry": "{\"timestamp\": \"2026-01-09T10:30:00Z\", \"event\": \"task_complete\", \"task\": \"EDA notebook\"}"
  }
}
```

**Response:**
```json
{
  "success": true,
  "bytes_written": 95,
  "timestamp": "2026-01-09T10:30:00Z"
}
```

### Constraints

- **Append-only**: Cannot overwrite or delete
- **Target files**: Only memory files allowed
- **Max entry size**: 10KB
- **Validation**: JSON lines must be valid JSON
- **User approval**: Requires user confirmation before write

---

## Constraint Summary

| Tool | Access | Side Effects | Approval Required |
|------|--------|--------------|-------------------|
| hello | Public | None | No |
| read_repo_file | Filtered | None | No |
| write_memory_entry | Memory only | Append | Yes |

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Invalid parameters |
| 403 | Access denied (blocked path) |
| 404 | File not found |
| 413 | Entry too large |
| 429 | Rate limit exceeded |
| 500 | Internal server error |
