#!/usr/bin/env python3
"""
Ruff MCP Server
A Model Context Protocol server for Ruff Python linter and formatter.
"""

import asyncio
import json
from typing import Any

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
)
import mcp.types as types

from .utils import ruff_check, ruff_format, ruff_fix

# Server instance
server = Server("ruff-mcp")


@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="ruff://docs",
            name="Ruff MCP Documentation",
            description="Documentation for the Ruff MCP server",
            mimeType="text/plain",
        )
    ]


@server.read_resource()
async def handle_read_resource(uri: Any) -> str:
    """Read a resource by URI."""
    if str(uri) == "ruff://docs":
        return """
# Ruff MCP Server

Available tools:
- ruff_check: Run ruff check on files or directories
- ruff_format: Format Python code with ruff
- ruff_fix: Auto-fix linting issues with ruff

Use these tools to lint and format Python code using Ruff.
"""
    raise ValueError(f"Unknown resource: {uri}")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="ruff_check",
            description="Run ruff check on files or directories to find linting issues",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File or directory path to check",
                    },
                    "fix": {
                        "type": "boolean",
                        "description": "Automatically fix linting issues",
                        "default": False,
                    },
                    "output_format": {
                        "type": "string",
                        "description": "Output format (concise, full, json, json-lines, junit, sarif)",
                        "default": "concise",
                    },
                },
                "required": ["path"],
            },
        ),
        Tool(
            name="ruff_format",
            description="Format Python code with ruff",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File or directory path to format",
                    },
                    "check": {
                        "type": "boolean",
                        "description": "Check if files are formatted without modifying them",
                        "default": False,
                    },
                    "diff": {
                        "type": "boolean",
                        "description": "Show diff of changes without modifying files",
                        "default": False,
                    },
                },
                "required": ["path"],
            },
        ),
        Tool(
            name="ruff_fix",
            description="Auto-fix linting issues with ruff",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File or directory path to fix",
                    },
                    "unsafe": {
                        "type": "boolean",
                        "description": "Apply unsafe fixes",
                        "default": False,
                    },
                },
                "required": ["path"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls."""
    if arguments is None:
        arguments = {}

    try:
        if name == "ruff_check":
            path = arguments.get("path", "")
            fix = arguments.get("fix", False)
            output_format = arguments.get("output_format", "concise")
            result = ruff_check(path, fix, output_format)
            return [
                TextContent(
                    type="text",
                    text=result,
                )
            ]

        elif name == "ruff_format":
            path = arguments.get("path", "")
            check = arguments.get("check", False)
            diff = arguments.get("diff", False)
            result = ruff_format(path, check, diff)
            return [
                TextContent(
                    type="text",
                    text=result,
                )
            ]

        elif name == "ruff_fix":
            path = arguments.get("path", "")
            unsafe = arguments.get("unsafe", False)
            result = ruff_fix(path, unsafe)
            return [
                TextContent(
                    type="text",
                    text=result,
                )
            ]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [
            TextContent(
                type="text",
                text=json.dumps(
                    {"error": str(e), "tool": name}, indent=2
                ),
            )
        ]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="ruff-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())