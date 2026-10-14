"""Project creation and build MCP tools for xtool."""

import asyncio
import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent


def register_project_tools(app: Server):
    """Register tools for creating and building iOS projects."""

    @app.list_tools()
    async def list_project_tools() -> List[Tool]:
        return [
            Tool(
                name="xtool_new_project",
                description="Scaffold a new iOS SwiftPM application project using xtool.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the new iOS application.",
                        },
                        "bundle_id": {
                            "type": "string",
                            "description": "Bundle identifier (e.g. 'com.company.myapp').",
                        },
                        "output_dir": {
                            "type": "string",
                            "description": "Directory to create the project in (default: current directory).",
                        },
                    },
                    "required": ["name"],
                },
            ),
            Tool(
                name="xtool_build_app",
                description="Build a SwiftPM iOS application package into an app bundle or IPA.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "Path to the project containing Package.swift.",
                        },
                        "configuration": {
                            "type": "string",
                            "description": "Build configuration: 'debug' or 'release'.",
                            "enum": ["debug", "release"],
                            "default": "debug",
                        },
                    },
                },
            ),
            Tool(
                name="xtool_dev_run",
                description="Run the interactive development cycle (build, sign, deploy to device/simulator) with live reloading.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "Path to the project directory.",
                        },
                        "device_id": {
                            "type": "string",
                            "description": "Target device UDID or name.",
                        },
                    },
                },
            ),
        ]

    @app.call_tool()
    async def call_project_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        xtool_bin = shutil.which("xtool") or "xtool"

        if name == "xtool_new_project":
            app_name = arguments["name"]
            bundle_id = arguments.get("bundle_id", f"com.example.{app_name.lower()}")
            out_dir = Path(arguments.get("output_dir", ".")) / app_name

            # Check if xtool binary is installed, else create standard Package.swift structure
            cmd = [xtool_bin, "new", app_name, "--bundle-id", bundle_id]
            try:
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
                out_text = stdout.decode().strip() or stderr.decode().strip()
                return [TextContent(type="text", text=out_text or f"Created project {app_name}")]
            except FileNotFoundError:
                # Fallback scaffolding when xtool binary is not yet on PATH
                out_dir.mkdir(parents=True, exist_ok=True)
                sources_dir = out_dir / "Sources" / app_name
                sources_dir.mkdir(parents=True, exist_ok=True)

                package_swift = f"""// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "{app_name}",
    platforms: [.iOS(.v17)],
    products: [
        .executable(name: "{app_name}", targets: ["{app_name}"])
    ],
    dependencies: [],
    targets: [
        .target(
            name: "{app_name}",
            dependencies: [],
            path: "Sources/{app_name}"
        )
    ]
)
"""
                app_swift = """import SwiftUI

@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: "globe")
                .imageScale(.large)
                .foregroundStyle(.tint)
            Text("Hello from xtool!")
                .font(.title)
        }
        .padding()
    }
}
"""
                (out_dir / "Package.swift").write_text(package_swift, encoding="utf-8")
                (sources_dir / "App.swift").write_text(app_swift, encoding="utf-8")
                return [TextContent(type="text", text=f"Scaffolded iOS SwiftPM project '{app_name}' at {out_dir}")]

        elif name == "xtool_build_app":
            proj_path = arguments.get("project_path", ".")
            config = arguments.get("configuration", "debug")
            cmd = ["swift", "build", "-c", config]
            try:
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    cwd=proj_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
                output = stdout.decode() + stderr.decode()
                return [TextContent(type="text", text=output.strip() or f"Build completed with exit code {proc.returncode}")]
            except Exception as e:
                return [TextContent(type="text", text=f"Build error: {str(e)}")]

        elif name == "xtool_dev_run":
            proj_path = arguments.get("project_path", ".")
            dev_cmd = [xtool_bin, "dev"]
            if "device_id" in arguments:
                dev_cmd.extend(["--device", arguments["device_id"]])
            try:
                proc = await asyncio.create_subprocess_exec(
                    *dev_cmd,
                    cwd=proj_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
                return [TextContent(type="text", text=(stdout.decode() or stderr.decode()).strip())]
            except Exception as e:
                return [TextContent(type="text", text=f"xtool dev: {str(e)}")]

        return []
