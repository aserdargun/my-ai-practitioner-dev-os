# MCP Tool Examples

Practical examples of how agents use MCP tools in the AI Practitioner Booster 2026 system.

---

## Example 1: Checking Progress

The Evaluator agent reads the progress log to compute scores.

```python
# Agent calls read_repo_file to get progress data
result = mcp_client.call(
    tool="read_repo_file",
    parameters={"path": ".claude/memory/progress_log.jsonl"}
)

# Parse the log
import json
events = [json.loads(line) for line in result["content"].split("\n") if line]

# Count completed tasks
completed = [e for e in events if e.get("event") == "task_complete"]
print(f"Completed tasks: {len(completed)}")
```

---

## Example 2: Logging Progress

The Coach agent logs a week completion event (with user approval).

```python
import json
from datetime import datetime

# Prepare the entry
entry = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "event": "week_complete",
    "week": 3,
    "status": "complete",
    "highlight": "Shipped baseline model"
}

# Show to user for approval
print("Proposed entry:")
print(json.dumps(entry, indent=2))
approval = input("Approve? (yes/no): ")

if approval.lower() == "yes":
    result = mcp_client.call(
        tool="write_memory_entry",
        parameters={
            "file": "progress_log.jsonl",
            "entry": json.dumps(entry)
        }
    )
    print(f"Logged: {result['bytes_written']} bytes")
```

---

## Example 3: Adding Best Practice

The Coach agent adds a best practice insight.

```python
# User provides the insight
insight = "Taking 5-minute breaks every 45 minutes helps maintain focus."

# Format as markdown entry
from datetime import date
entry = f"""
## {date.today().isoformat()} — Focus Management

{insight}

**Why it works**: Prevents mental fatigue during long coding sessions.
"""

# Show to user for approval
print("Proposed entry for best_practices.md:")
print(entry)
approval = input("Approve? (yes/no): ")

if approval.lower() == "yes":
    result = mcp_client.call(
        tool="write_memory_entry",
        parameters={
            "file": "best_practices.md",
            "entry": entry
        }
    )
    print("Best practice added!")
```

---

## Example 4: Reading Current Status

The Planner agent reads the tracker to understand current state.

```python
# Read tracker
tracker = mcp_client.call(
    tool="read_repo_file",
    parameters={"path": "paths/Advanced/tracker.md"}
)

# Read profile
profile = mcp_client.call(
    tool="read_repo_file",
    parameters={"path": ".claude/memory/learner_profile.json"}
)

import json
profile_data = json.loads(profile["content"])

print(f"Current month: {profile_data['schedule']['current_month']}")
print(f"Current week: {profile_data['schedule']['current_week']}")
print(f"Hours per week: {profile_data['constraints']['hours_per_week']}")
```

---

## Example 5: Testing Connectivity

Simple test to verify MCP server is running.

```python
# Test hello tool
result = mcp_client.call(
    tool="hello",
    parameters={"name": "Learner"}
)

print(f"Server says: {result['message']}")
print(f"Server time: {result['timestamp']}")
```

---

## Example 6: Error Handling

Handling common error cases.

```python
try:
    result = mcp_client.call(
        tool="read_repo_file",
        parameters={"path": ".env"}  # Blocked path
    )
except MCPError as e:
    if e.code == 403:
        print("Access denied: Cannot read sensitive files")
    elif e.code == 404:
        print("File not found")
    else:
        print(f"Error {e.code}: {e.message}")
```

---

## Example 7: Batch Reading

Reading multiple files for context.

```python
files_to_read = [
    ".claude/memory/learner_profile.json",
    ".claude/memory/progress_log.jsonl",
    "paths/Advanced/tracker.md"
]

context = {}
for file_path in files_to_read:
    try:
        result = mcp_client.call(
            tool="read_repo_file",
            parameters={"path": file_path}
        )
        context[file_path] = result["content"]
    except MCPError:
        context[file_path] = None

# Now agent has full context for decision-making
```

---

## Agent Workflow Integration

### Evaluator Agent Flow

```
1. read_repo_file("paths/Advanced/tracker.md")
2. read_repo_file(".claude/memory/progress_log.jsonl")
3. Compute scores locally
4. Present scores to user
5. (If user approves logging)
6. write_memory_entry("progress_log.jsonl", evaluation_event)
```

### Coach Agent Flow

```
1. read_repo_file(".claude/memory/best_practices.md")
2. Identify relevant practices for current situation
3. Provide guidance to user
4. (If user wants to add new practice)
5. Show proposed entry
6. (After user approval)
7. write_memory_entry("best_practices.md", new_entry)
```

### Planner Agent Flow

```
1. read_repo_file(".claude/memory/learner_profile.json")
2. read_repo_file("paths/Advanced/month-XX/README.md")
3. Generate week plan
4. Present plan to user
5. (After user approval)
6. write_memory_entry("progress_log.jsonl", plan_created_event)
```
