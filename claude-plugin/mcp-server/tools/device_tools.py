"""iOS Device management MCP tools for xtool."""

import asyncio
import json
import shutil
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent


def register_device_tools(app: Server):
    """Register tools for interacting with iOS devices."""

    @app.list_tools()
    async def list_device_tools() -> List[Tool]:
        return [
            Tool(
                name="xtool_list_devices",
                description="List all connected iOS physical devices and active simulators.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            Tool(
                name="xtool_install_app",
                description="Install an IPA file or app bundle onto a connected iOS device.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "ipa_path": {
                            "type": "string",
                            "description": "Path to the .ipa file or .app bundle.",
                        },
                        "device_id": {
                            "type": "string",
                            "description": "Optional device UDID to target.",
                        },
                    },
                    "required": ["ipa_path"],
                },
            ),
            Tool(
                name="xtool_launch_app",
                description="Launch an installed iOS app on a connected device.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "bundle_id": {
                            "type": "string",
                            "description": "Bundle identifier of the application (e.g. 'com.example.myapp').",
                        },
                        "device_id": {
                            "type": "string",
                            "description": "Optional device UDID to target.",
                        },
                    },
                    "required": ["bundle_id"],
                },
            ),
            Tool(
                name="xtool_uninstall_app",
                description="Uninstall an application from a connected device.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "bundle_id": {
                            "type": "string",
                            "description": "Bundle identifier of the app to remove.",
                        },
                        "device_id": {
                            "type": "string",
                            "description": "Optional device UDID to target.",
                        },
                    },
                    "required": ["bundle_id"],
                },
            ),
        ]

    @app.call_tool()
    async def call_device_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        xtool_bin = shutil.which("xtool") or "xtool"

        if name == "xtool_list_devices":
            cmd = [xtool_bin, "devices"]
            try:
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
                out = (stdout.decode() or stderr.decode()).strip()
                return [TextContent(type="text", text=out or "No devices detected. Connect an iPhone/iPad via USB or Wi-Fi.")]
            except FileNotFoundError:
                return [TextContent(type="text", text="xtool binary not found on PATH. Run 'xtool setup' to install prerequisites.")]

        elif name == "xtool_install_app":
            cmd = [xtool_bin, "install", arguments["ipa_path"]]
            if "device_id" in arguments:
                cmd.extend(["--device", arguments["device_id"]])
            try:
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
                return [TextContent(type="text", text=(stdout.decode() or stderr.decode()).strip())]
            except Exception as e:
                return [TextContent(type="text", text=f"Install error: {str(e)}")]

        elif name == "xtool_launch_app":
            cmd = [xtool_bin, "launch", arguments["bundle_id"]]
            if "device_id" in arguments:
                cmd.extend(["--device", arguments["device_id"]])
            try:
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
                return [TextContent(type="text", text=(stdout.decode() or stderr.decode()).strip())]
            except Exception as e:
                return [TextContent(type="text", text=f"Launch error: {str(e)}")]

        elif name == "xtool_uninstall_app":
            cmd = [xtool_bin, "uninstall", arguments["bundle_id"]]
            if "device_id" in arguments:
                cmd.extend(["--device", arguments["device_id"]])
            try:
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
                return [TextContent(type="text", text=(stdout.decode() or stderr.decode()).strip())]
            except Exception as e:
                return [TextContent(type="text", text=f"Uninstall error: {str(e)}")]

        return []
