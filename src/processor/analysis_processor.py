from agent.analysis_agent import get_analysis_agent
from google.adk.runners import Runner
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService 
from log_config import get_logger
logger = get_logger(__name__)


class AnalysisProcessor:
    def __init__(self):
        # app and agent
        self.app_name = "analysis_app"
        self.agent = get_analysis_agent()
        # session
        session_service = InMemorySessionService()
        artifacts_service = InMemoryArtifactService()
        self.session = self.session_service.create_session(
            state={}, app_name=self.app_name, user_id="user_01", 
        )
        # runner
        self.runner = Runner(
            app_name=self.app_name,
            agent=self.agent, 

        )

        pass

    async def run(self, query: str) -> str:
        content = types.Content(role='user', parts=[types.Part(text=query)])
        events_async = self.runner.run_async(
            session_id=self.session, user_id = self.session.user_id, new_message = content
        )
        async for event in events_async:
            logger.info(f"Event received: {str(event.content)}")
            if event.is_final_response():
                return event.content.parts[0].text
            pass