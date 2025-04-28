from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from ..model import create_inference_model
import prompt


# 直接同步就行了 = = || 先不整mcp了 感觉没必要
def get_analysis_agent():
    return LlmAgent(
        model=create_inference_model(),
        name="text_analysis_agent",
        instruction=prompt.AGENT_INSTRUCTION,
        description=prompt.AGENT_DESCRIPTION,

    )

