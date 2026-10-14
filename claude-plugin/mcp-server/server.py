"""xtool — MCP Server for Claude Code.

Exposes cross-platform iOS development and deployment capabilities as MCP tools.
"""

import asyncio
import os
import sys

MCP_DIR = os.path.dirname(os.path.abspath(__file__))
if MCP_DIR not in sys.path:
    sys.path.insert(0, MCP_DIR)

from mcp.server import Server
from mcp.server.stdio import stdio_server

from tools.project_tools import register_project_tools
from tools.device_tools import register_device_tools
from tools.developer_tools import register_developer_tools

app = Server("ios-app-xtool")

# Register tool groups
register_project_tools(app)
register_device_tools(app)
register_developer_tools(app)


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
