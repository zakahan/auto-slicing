from agent.clip_agent import get_clip_agent, get_clip_prompt
from google.adk.runners import Runner
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService 
from typing import Any
from log_config import get_logger
logger = get_logger()


class ClipProcessor:
    def __init__(self):
        # app and agent
        self.app_name = "clip_app"
        # user and session: only me
        self.user_id = "user_01"
        self.session_id = "session_01"
    
        # session
        self.session_service = InMemorySessionService()
        self.session_service.create_session(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=self.session_id
        )
        
        pass

    async def run(self, query: dict[str, Any], prompt_key: str='easy') -> str:
        agent, tools = get_clip_agent()

        runner = Runner(
            app_name=self.app_name,
            agent=agent,
            session_service=self.session_service
        )

        prompt = get_clip_prompt(query=query, key=prompt_key)
        content = types.Content(role='user', parts=[types.Part(text=prompt)])
        events_async = runner.run_async(
            session_id=self.session_id,
            user_id=self.user_id,
            new_message=content
        )
        async for event in events_async:
            logger.info(f"Event received: {str(event.content)}")
            if event.is_final_response():
                await tools.close()
                return event.content.parts[0].text
            pass
        return ""


    def get_session_state(self) -> dict:
        session = self.session_service.get_session(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=self.session_id
        )
        return dict(session)