# MCP (Model Context Protocol)

This folder contains tool contracts, safety guidelines, and example implementations for MCP integration.

## Overview

MCP (Model Context Protocol) defines how Claude interacts with external tools and services. This folder provides:

- **Tool Contracts**: Schemas and constraints for available tools
- **Safety Guidelines**: Security and privacy rules
- **Server Stub**: Example MCP server implementation
- **Client Examples**: How to call MCP tools

## Contents

| File/Folder | Purpose |
|-------------|---------|
| [tool-contracts.md](tool-contracts.md) | Tool schemas and constraints |
| [examples.md](examples.md) | Usage examples |
| [safety.md](safety.md) | Security and privacy rules |
| [server_stub/](server_stub/) | Example MCP server |
| [client_examples/](client_examples/) | Example MCP clients |

## Available Tools

The learning OS exposes these tools via MCP:

| Tool | Description | Safety Level |
|------|-------------|--------------|
| `hello` | Test tool, returns greeting | Safe |
| `read_repo_file` | Read files from repo | Read-only |
| `write_memory_entry` | Append to memory files | Append-only |

## Quick Start

### Running the Server

```bash
cd .claude/mcp/server_stub
python server.py
```

The server runs on `http://localhost:8080` by default.

### Testing with Client

```bash
cd .claude/mcp/client_examples
python python_client.py
```

## Tool Contracts

Each tool has a defined contract specifying:

- **Name**: Tool identifier
- **Description**: What it does
- **Parameters**: Input schema
- **Returns**: Output schema
- **Constraints**: Safety limits

See [tool-contracts.md](tool-contracts.md) for full specifications.

## Safety Principles

1. **Minimal Access**: Tools have only necessary permissions
2. **Append-Only**: Memory writes are append-only
3. **No Secrets**: Tools never expose or log secrets
4. **Audit Trail**: All tool calls are logged
5. **User Approval**: Sensitive operations require confirmation

See [safety.md](safety.md) for detailed guidelines.

## Integration with Agents

Agents can use MCP tools when:
- The tool is appropriate for the task
- Safety constraints are satisfied
- User has approved (for sensitive operations)

Example agent prompt:
```
Use the read_repo_file tool to check the current tracker status.
```

## Extending MCP

To add new tools:

1. Define the contract in [tool-contracts.md](tool-contracts.md)
2. Implement in [server_stub/server.py](server_stub/server.py)
3. Add usage example to [examples.md](examples.md)
4. Update safety guidelines if needed
