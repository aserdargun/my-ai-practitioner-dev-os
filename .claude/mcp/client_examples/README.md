# MCP Client Examples

Example client implementations for calling MCP tools.

## Python Client

See [python_client.py](python_client.py) for a complete example.

### Quick Start

```python
from python_client import MCPClient

# Create client
client = MCPClient("http://localhost:8080")

# Test connectivity
result = client.hello("Learner")
print(result["message"])

# Read a file
content = client.read_file("README.md")
print(content[:100])

# Write to memory (requires approval workflow)
client.write_memory(
    file="progress_log.jsonl",
    entry='{"event": "test"}'
)
```

### Running the Example

1. Start the MCP server:
   ```bash
   cd .claude/mcp/server_stub
   python server.py
   ```

2. In another terminal, run the client:
   ```bash
   cd .claude/mcp/client_examples
   python python_client.py
   ```

## Usage in Agents

Agents can use the client to interact with the learning system:

```python
# In an agent implementation
client = MCPClient()

# Read current progress
progress = client.read_file(".claude/memory/progress_log.jsonl")
events = [json.loads(line) for line in progress.split("\n") if line]

# Analyze and provide recommendations
# ...

# Log new event (with user approval)
if user_approves:
    client.write_memory(
        file="progress_log.jsonl",
        entry=json.dumps(new_event)
    )
```

## Error Handling

The client raises exceptions for errors:

```python
from python_client import MCPClient, MCPError

client = MCPClient()

try:
    content = client.read_file(".env")  # Blocked
except MCPError as e:
    if e.status == 403:
        print("Access denied")
    elif e.status == 404:
        print("File not found")
```

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_SERVER_URL` | `http://localhost:8080` | Server URL |
| `MCP_TIMEOUT` | `30` | Request timeout (seconds) |
