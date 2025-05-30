from contextlib import AsyncExitStack
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.tools.base_toolset import BaseToolset

from ..model import create_inference_model
from .prompt import AGENT_DESCRIPTION,AGENT_INSTRUCTION
from .tools import get_video_editor_tools


def get_clip_agent()-> tuple[LlmAgent, BaseToolset]:
    tools = get_video_editor_tools()

    clip_agent = LlmAgent(
        model=create_inference_model(),
        name="clip_agent",
        description=AGENT_DESCRIPTION,
        instruction=AGENT_INSTRUCTION,
        tools=[tools],
        output_key="clip_result"
    )
    return clip_agent, tools