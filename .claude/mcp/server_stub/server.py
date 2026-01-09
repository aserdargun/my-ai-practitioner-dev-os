#!/usr/bin/env python3
"""
MCP Server Stub for AI Practitioner Booster 2026

A minimal MCP server exposing learning system tools.
Uses only Python stdlib - no external dependencies.
"""

import json
import os
import re
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

# Configuration
PORT = int(os.environ.get("PORT", 8080))
REPO_ROOT = Path(os.environ.get("REPO_ROOT", "../../..")).resolve()
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# Blocked path patterns
BLOCKED_PATTERNS = [
    r"\.env.*",
    r".*\.key$",
    r".*\.pem$",
    r".*/secrets/.*",
    r".*/.git/.*",
    r".*/node_modules/.*",
    r".*/__pycache__/.*",
]

# Allowed memory files
MEMORY_FILES = ["progress_log.jsonl", "decisions.jsonl", "best_practices.md"]


def log(level: str, message: str) -> None:
    """Simple logging."""
    levels = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
    if levels.get(level, 0) >= levels.get(LOG_LEVEL, 1):
        print(f"[{datetime.now().isoformat()}] {level}: {message}")


def is_path_blocked(path: str) -> bool:
    """Check if path matches any blocked pattern."""
    for pattern in BLOCKED_PATTERNS:
        if re.match(pattern, path):
            return True
    return False


def tool_hello(params: dict) -> dict:
    """Hello tool - test connectivity."""
    name = params.get("name", "World")
    return {
        "message": f"Hello, {name}!",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


def tool_read_repo_file(params: dict) -> dict:
    """Read a file from the repository."""
    path = params.get("path")
    if not path:
        raise ValueError("Missing required parameter: path")

    # Validate path format
    if not re.match(r"^[a-zA-Z0-9_./-]+$", path):
        raise ValueError("Invalid path format")

    # Check for blocked paths
    if is_path_blocked(path):
        raise PermissionError("Access denied: blocked path")

    # Resolve and validate path
    full_path = (REPO_ROOT / path).resolve()
    if not str(full_path).startswith(str(REPO_ROOT)):
        raise PermissionError("Access denied: path traversal")

    if not full_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not full_path.is_file():
        raise ValueError("Path is not a file")

    # Check file size
    size = full_path.stat().st_size
    if size > 1_000_000:  # 1MB limit
        raise ValueError("File too large (max 1MB)")

    # Read file
    encoding = params.get("encoding", "utf-8")
    if encoding == "base64":
        import base64
        content = base64.b64encode(full_path.read_bytes()).decode("ascii")
    else:
        content = full_path.read_text(encoding="utf-8")

    return {
        "content": content,
        "size": size,
        "modified": datetime.fromtimestamp(full_path.stat().st_mtime).isoformat() + "Z"
    }


def tool_write_memory_entry(params: dict) -> dict:
    """Append an entry to a memory file."""
    file_name = params.get("file")
    entry = params.get("entry")

    if not file_name:
        raise ValueError("Missing required parameter: file")
    if not entry:
        raise ValueError("Missing required parameter: entry")

    # Validate file name
    if file_name not in MEMORY_FILES:
        raise ValueError(f"Invalid file: must be one of {MEMORY_FILES}")

    # Validate entry size
    if len(entry) > 10_000:  # 10KB limit
        raise ValueError("Entry too large (max 10KB)")

    # For JSON lines, validate JSON
    if file_name.endswith(".jsonl"):
        try:
            json.loads(entry)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON for .jsonl file")

    # Resolve path
    memory_path = REPO_ROOT / ".claude" / "memory" / file_name
    if not memory_path.parent.exists():
        memory_path.parent.mkdir(parents=True)

    # Append entry
    with open(memory_path, "a", encoding="utf-8") as f:
        if file_name.endswith(".jsonl"):
            f.write(entry.strip() + "\n")
        else:
            f.write("\n" + entry)

    return {
        "success": True,
        "bytes_written": len(entry),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


# Tool registry
TOOLS = {
    "hello": {
        "handler": tool_hello,
        "description": "Test connectivity",
    },
    "read_repo_file": {
        "handler": tool_read_repo_file,
        "description": "Read a file from the repository",
    },
    "write_memory_entry": {
        "handler": tool_write_memory_entry,
        "description": "Append to a memory file",
    },
}


class MCPHandler(BaseHTTPRequestHandler):
    """HTTP request handler for MCP server."""

    def send_json(self, data: Any, status: int = 200) -> None:
        """Send JSON response."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, status: int, message: str) -> None:
        """Send JSON error response."""
        self.send_json({"error": message}, status)

    def do_GET(self) -> None:
        """Handle GET requests."""
        path = urlparse(self.path).path

        if path == "/health":
            self.send_json({"status": "healthy"})
        elif path == "/tools":
            tools = {name: info["description"] for name, info in TOOLS.items()}
            self.send_json({"tools": tools})
        else:
            self.send_error_json(404, "Not found")

    def do_POST(self) -> None:
        """Handle POST requests."""
        path = urlparse(self.path).path

        # Parse tool name from path
        if not path.startswith("/tools/"):
            self.send_error_json(404, "Not found")
            return

        tool_name = path[7:]  # Remove "/tools/" prefix

        if tool_name not in TOOLS:
            self.send_error_json(404, f"Unknown tool: {tool_name}")
            return

        # Read request body
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 100_000:  # 100KB limit
            self.send_error_json(413, "Request too large")
            return

        try:
            body = self.rfile.read(content_length)
            params = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self.send_error_json(400, "Invalid JSON")
            return

        # Call tool
        log("INFO", f"Calling tool: {tool_name}")
        try:
            result = TOOLS[tool_name]["handler"](params)
            self.send_json(result)
        except ValueError as e:
            self.send_error_json(400, str(e))
        except PermissionError as e:
            self.send_error_json(403, str(e))
        except FileNotFoundError as e:
            self.send_error_json(404, str(e))
        except Exception as e:
            log("ERROR", f"Tool error: {e}")
            self.send_error_json(500, "Internal server error")

    def log_message(self, format: str, *args) -> None:
        """Override to use our logger."""
        log("DEBUG", f"{self.address_string()} - {format % args}")


def main() -> None:
    """Run the MCP server."""
    server = HTTPServer(("", PORT), MCPHandler)
    log("INFO", f"MCP Server starting on port {PORT}")
    log("INFO", f"Repository root: {REPO_ROOT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("INFO", "Shutting down")
        server.shutdown()


if __name__ == "__main__":
    main()
