"""Developer services and SDK status MCP tools for xtool."""

import asyncio
import json
import shutil
from typing import Any, Dict, List
from mcp.server import Server
from mcp.types import Tool, TextContent


def register_developer_tools(app: Server):
    """Register tools for toolchain setup and Apple Developer account status."""

    @app.list_tools()
    async def list_developer_tools() -> List[Tool]:
        return [
            Tool(
                name="xtool_setup_status",
                description="Check environment readiness: checks Swift compiler, xtool CLI, Darwin SDK, and platform prerequisites.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name="xtool_auth_status",
                description="Check Apple Developer Services authentication status.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
        ]

    @app.call_tool()
    async def call_developer_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        xtool_bin = shutil.which("xtool") or "xtool"
        swift_bin = shutil.which("swift")

        if name == "xtool_setup_status":
            status = {
                "swift_installed": bool(swift_bin),
                "swift_path": swift_bin or "not found",
                "xtool_installed": bool(shutil.which("xtool")),
                "xtool_path": shutil.which("xtool") or "not found",
            }
            if swift_bin:
                try:
                    proc = await asyncio.create_subprocess_exec(
                        swift_bin, "--version",
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )
                    stdout, _ = await proc.communicate()
                    status["swift_version"] = stdout.decode().strip().split("\n")[0]
                except Exception:
                    pass

            return [TextContent(type="text", text=json.dumps(status, indent=2))]

        elif name == "xtool_auth_status":
            try:
                proc = await asyncio.create_subprocess_exec(
                    xtool_bin, "auth",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
                out = (stdout.decode() or stderr.decode()).strip()
                return [TextContent(type="text", text=out or "No active Apple Developer credentials found. Configure via 'xtool auth'.")]
            except FileNotFoundError:
                return [TextContent(type="text", text="xtool binary not found on PATH. Run 'xtool setup' to get started.")]

        return []
