import os
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import MCPToolset

from typing import Callable


def create_litellm_model():
    model_name = os.getenv("API_MODEL_NAME")
    model_url = os.getenv("API_BASE_URL")
    api_key = os.getenv("ARK_API_KEY")
    assert model_name, "API_MODEL_NAME is required"
    assert model_url, "API_BASE_URL is required"
    assert api_key, "ARK_API_KEY is required"
    return LiteLlm(model=f"openai/{model_name}", api_key=api_key, base_url=model_url)


def create_agent(
    agent_name: str,
    agent_description: str,
    agent_instruction: str,
    tools: list[Callable | MCPToolset] = None,
    sub_agents=None,
):
    if sub_agents is None:
        sub_agents = []
    return Agent(
        model=create_litellm_model(),
        name=agent_name,
        description=agent_description,
        instruction=agent_instruction,
        tools=tools,
        sub_agents=sub_agents,
    )
