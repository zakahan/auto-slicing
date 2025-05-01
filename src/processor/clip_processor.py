from agent.clip_agent import aget_clip_agent
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

    async def run(self, query: dict[str, Any]) -> str:
        agent, exit_stack = await aget_clip_agent()

        runner = Runner(
            app_name=self.app_name,
            agent=agent,
            session_service=self.session_service
        )

        prompt = f"""你需要对一段视频执行剪辑操作，要求如下
        在原素材上切分出一段视频，随后修改标题，要求全过程都使用工具完成。
        参数如下：
        1. origin_video_path: {query['origin_video_path']}：
        2. task_id: {query['task_id']}
        3. start_time:{query['start_time']}
        4. stop_time:{query['stop_time']}
        5. title: {query['title']} 
        请完成剪辑任务

        """
        content = types.Content(role='user', parts=[types.Part(text=prompt)])
        events_async = runner.run_async(
            session_id=self.session_id,
            user_id=self.user_id,
            new_message=content
        )
        async for event in events_async:
            logger.info(f"Event received: {str(event.content)}")
            if event.is_final_response():
                await exit_stack.aclose()
                return event.content.parts[0].text
            pass
        return ""

    async def run_r(self, query: dict[str, Any]) -> str:
        agent, exit_stack = await aget_clip_agent()

        runner = Runner(
            app_name=self.app_name,
            agent=agent, 
            session_service=self.session_service
        )

        prompt=f"""你需要对一段视频执行剪辑操作，要求如下
        先在原素材上切分出两段视频，随后按顺序合并。
        参数如下：
        1. origin_video_path: {query['origin_video_path']}：
        2. 第一段视频
            2.1 task_id: {query['clip'][0]['task_id']}
            2.2. start_time:{query['clip'][0]['start_time']}
            2.3. stop_time:{query['clip'][0]['stop_time']}
        3. 第二段视频
            3.1 task_id: {query['clip'][1]['task_id']}
            3.2 start_time:{query['clip'][1]['start_time']}
            3.3 stop_time:{query['clip'][1]['stop_time']}
        4. 合并两段视频
            4.1 task_id: {query['merge']['task_id']},
            4.2 video_paths: 请你根据前两段视频合并操作的结果来决定
        5. 将视频重命名为
        请完成剪辑任务
        
        """
        content = types.Content(role='user', parts=[types.Part(text=prompt)])
        events_async = runner.run_async(
            session_id=self.session_id,
            user_id=self.user_id,
            new_message=content
        )
        async for event in events_async:
            logger.info(f"Event received: {str(event.content)}")
            if event.is_final_response():
                await exit_stack.aclose()
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