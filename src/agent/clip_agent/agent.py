from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from ..model import create_inference_model
from prompt import AGENT_DESCRIPTION,AGENT_INSTRUCTION



def get_clip_agent():
    return LlmAgent(
        model=create_inference_model(),
        name="clip_agent",
        description=AGENT_DESCRIPTION,
        instruction=AGENT_INSTRUCTION,
        tools=[]
    )