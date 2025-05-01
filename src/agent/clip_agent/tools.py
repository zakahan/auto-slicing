import os
import asyncio
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams, StdioServerParameters
from mcp_servers import MCP_SERVERS_DIR, VIDEO_EDITOR
from log_config import get_logger
logger = get_logger()

mcp_tool_path = os.path.join(MCP_SERVERS_DIR, VIDEO_EDITOR)

# mcp client
async def aget_video_editor_tools():
    """Gets tools from mcp server"""
    logger.debug("Attempting to connection to video editor mcp server...")

    tools, exist_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command="python",
            args=[
                mcp_tool_path
            ]
        )
    )
    logger.debug("Video Editor MCP Toolset Created Successfully.")
    
    return tools, exist_stack

