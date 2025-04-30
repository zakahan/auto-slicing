
# 测试session是否能保存
import os
import os.path as op
from dotenv import load_dotenv
load_dotenv(op.join(op.dirname(op.dirname(__file__)), "src/.env"))

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from agent.model import create_inference_model
from google.adk.runners import Runner

from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService 





def get_clip_agent():
    return LlmAgent(
        model=create_inference_model(),
        name="clip_agent",
        description="请你替我计算结果",
        instruction="你会参与计算操作，并且将计算式得到的结果输出",
        output_key="answer"
    )



session_service = InMemorySessionService()
session = session_service.create_session(
    state={}, app_name="APP", user_id="user_01", 
    session_id="s1"
)

query="1+2"

runner = Runner(
    app_name="APP",
    agent=get_clip_agent(), 
    session_service=session_service
)
content = types.Content(role='user', parts=[types.Part(text=query)])

async def func():
    events_async = runner.run_async(
        session_id="s1", user_id = session.user_id, new_message = content
    )      
    async for event in events_async:
        if event.is_final_response():
            print(event.content.parts[0].text)
            print(session_service.get_session(app_name="APP",user_id="user_01", session_id="s1").state)
            print(session.state)
        pass

import asyncio
asyncio.run(func())