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
    tools, exist_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command="python",
            args=[
                mcp_tool_path,
                "--kb_dir",
                os.getenv("KB_BASE_PATH"),      # MCP_LOGGER_FILE_DIR
                "--using_logger",
                os.getenv("MCP_USING_LOGGER"),
                "--logger_file_dir",
                os.getenv("MCP_LOGGER_FILE_DIR"),
            ],
        )
    )
    logger.debug("Video Editor MCP Toolset Created Successfully.")
    
    return tools, exist_stack

