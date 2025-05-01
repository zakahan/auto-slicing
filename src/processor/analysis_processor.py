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

    async def run(self, query: str, introduction:str) -> str:
        agent = get_analysis_agent()
        runner = Runner(
            app_name=self.app_name,
            agent=agent, 
            session_service=self.session_service
        )
        prompt=f"首先给你介绍一下主播的基本信息：{introduction}，切片内容分别如下：{str(query)}"
        content = types.Content(role='user', parts=[types.Part(text=prompt)])
        events_async = runner.run_async(
            session_id=self.session_id,
            user_id=self.user_id,
            new_message=content
        )
        async for event in events_async:
            logger.info(f"Event received: {str(event.content)}")
            if event.is_final_response():
                return event.content.parts[0].text
            pass
        return ""

    def get_session_state(self) -> dict:
        return dict(
            self.session_service.get_session(
                app_name=self.app_name,
                user_id=self.user_id,
                session_id=self.session_id
            )
        )