# MCP Server Stub

Example MCP server implementation for the AI Practitioner Booster 2026 learning system.

## Overview

This is a minimal MCP server that exposes the learning system's tools:

- `hello` — Test connectivity
- `read_repo_file` — Read repository files
- `write_memory_entry` — Append to memory files

## Requirements

- Python 3.11+
- No external dependencies (stdlib only)

## Running the Server

```bash
cd .claude/mcp/server_stub
python server.py
```

The server starts on `http://localhost:8080`.

## Testing

```bash
# Test hello
curl -X POST http://localhost:8080/tools/hello \
  -H "Content-Type: application/json" \
  -d '{"name": "Learner"}'

# Test read_repo_file
curl -X POST http://localhost:8080/tools/read_repo_file \
  -H "Content-Type: application/json" \
  -d '{"path": "README.md"}'
```

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8080 | Server port |
| `REPO_ROOT` | `../../..` | Repository root path |
| `LOG_LEVEL` | INFO | Logging level |

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/tools/{name}` | Call a tool |
| GET | `/tools` | List available tools |

## Security Notes

This is a **development server** for local testing:

- Do not expose to public internet
- Use proper authentication in production
- Review safety.md for guidelines

## Extending

To add new tools:

1. Add tool definition to `TOOLS` dict
2. Implement handler function
3. Update tool-contracts.md
4. Add examples to examples.md
