#!/usr/bin/env python3
"""
MCP Client Example for AI Practitioner Booster 2026

Demonstrates how to call MCP tools from Python.
Uses only Python stdlib - no external dependencies.
"""

import json
import os
from datetime import datetime
from typing import Any, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class MCPError(Exception):
    """Exception for MCP tool errors."""

    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message
        super().__init__(f"MCP Error {status}: {message}")


class MCPClient:
    """Client for calling MCP tools."""

    def __init__(
        self,
        server_url: Optional[str] = None,
        timeout: Optional[int] = None
    ):
        self.server_url = server_url or os.environ.get(
            "MCP_SERVER_URL", "http://localhost:8080"
        )
        self.timeout = timeout or int(os.environ.get("MCP_TIMEOUT", "30"))

    def _call(self, tool: str, params: dict) -> dict:
        """Call an MCP tool."""
        url = f"{self.server_url}/tools/{tool}"
        data = json.dumps(params).encode("utf-8")

        request = Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as e:
            body = e.read().decode("utf-8")
            try:
                error = json.loads(body)
                raise MCPError(e.code, error.get("error", body))
            except json.JSONDecodeError:
                raise MCPError(e.code, body)
        except URLError as e:
            raise MCPError(0, f"Connection error: {e.reason}")

    def hello(self, name: str = "World") -> dict:
        """Test connectivity with hello tool."""
        return self._call("hello", {"name": name})

    def read_file(self, path: str, encoding: str = "utf-8") -> str:
        """Read a file from the repository."""
        result = self._call("read_repo_file", {
            "path": path,
            "encoding": encoding
        })
        return result["content"]

    def write_memory(self, file: str, entry: str) -> dict:
        """Append an entry to a memory file."""
        return self._call("write_memory_entry", {
            "file": file,
            "entry": entry
        })

    def list_tools(self) -> dict:
        """List available tools."""
        url = f"{self.server_url}/tools"
        request = Request(url, method="GET")
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as e:
            raise MCPError(e.code, e.read().decode("utf-8"))

    def health_check(self) -> bool:
        """Check if server is healthy."""
        url = f"{self.server_url}/health"
        request = Request(url, method="GET")
        try:
            with urlopen(request, timeout=self.timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("status") == "healthy"
        except (HTTPError, URLError):
            return False


def demo():
    """Demonstrate MCP client usage."""
    print("MCP Client Demo")
    print("=" * 40)

    client = MCPClient()

    # Check server health
    print("\n1. Checking server health...")
    if not client.health_check():
        print("   Server is not running!")
        print("   Start with: python .claude/mcp/server_stub/server.py")
        return

    print("   Server is healthy!")

    # List tools
    print("\n2. Listing available tools...")
    tools = client.list_tools()
    for name, description in tools["tools"].items():
        print(f"   - {name}: {description}")

    # Test hello
    print("\n3. Testing hello tool...")
    result = client.hello("Learner")
    print(f"   {result['message']}")
    print(f"   Server time: {result['timestamp']}")

    # Read a file
    print("\n4. Reading README.md...")
    try:
        content = client.read_file("README.md")
        lines = content.split("\n")
        print(f"   First line: {lines[0]}")
        print(f"   Total lines: {len(lines)}")
    except MCPError as e:
        print(f"   Error: {e.message}")

    # Try to read blocked file
    print("\n5. Trying to read .env (should fail)...")
    try:
        client.read_file(".env")
        print("   Unexpectedly succeeded!")
    except MCPError as e:
        print(f"   Blocked as expected: {e.message}")

    # Write to memory (example - would need approval in real use)
    print("\n6. Writing to progress log...")
    entry = json.dumps({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event": "demo_run",
        "note": "MCP client demo completed"
    })

    # In real use, you'd get user approval first
    print(f"   Proposed entry: {entry}")
    print("   (In real use, would require user approval)")

    # Uncomment to actually write:
    # result = client.write_memory("progress_log.jsonl", entry)
    # print(f"   Written: {result['bytes_written']} bytes")

    print("\n" + "=" * 40)
    print("Demo complete!")


if __name__ == "__main__":
    demo()
