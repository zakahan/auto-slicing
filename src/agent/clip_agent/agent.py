from contextlib import AsyncExitStack
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from ..model import create_inference_model
from .prompt import AGENT_DESCRIPTION,AGENT_INSTRUCTION
from .tools import aget_video_editor_tools


async def aget_clip_agent()-> tuple[LlmAgent, AsyncExitStack]:
    tools, exit_stack = await aget_video_editor_tools()

    clip_agent = LlmAgent(
        model=create_inference_model(),
        name="clip_agent",
        description=AGENT_DESCRIPTION,
        instruction=AGENT_INSTRUCTION,
        tools=tools,
        output_key="clip_result"
    )
    return clip_agent, exit_stack