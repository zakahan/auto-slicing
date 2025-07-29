import uuid
from typing import Optional, Callable

from google.adk.memory import BaseMemoryService
from google.adk.sessions import InMemorySessionService, BaseSessionService
from google.adk.tools.base_toolset import BaseToolset

from agent_kit.agent_factory import create_agent
from processor.base.processor import BaseProcessor, BaseProcessorFactory
from processor.clip.prompt import AGENT_DESCRIPTION, AGENT_INSTRUCTION
from processor.processor_type import ProcessorName, ProcessorType
from tool.client.vedit.tools import get_video_editor_tools
from utils.log_config import get_logger

logger = get_logger()


class ClipProcessor(BaseProcessor):
    def __init__(
            self,
            session_service: Optional[BaseSessionService] = None,
            memory_service: Optional[BaseMemoryService] = None,
            stream: bool = False,
            tools: list[Callable | BaseToolset] = None,
    ):
        super().__init__(
            processor_name=ProcessorName.CLIP,
            processor_type=ProcessorType.AGENTIC,
            session_service=session_service,
            memory_service=memory_service,
            stream=stream,
        )
        self.agent = create_agent(
            agent_name=self._app_name,
            agent_description=AGENT_DESCRIPTION,
            agent_instruction=AGENT_INSTRUCTION,
            tools=tools,
        )

    async def run(self, query: dict, **kwargs) -> list[dict]:
        session_id = str(uuid.uuid4())  # generate a session id
        assert self.session_service, "session_service is required"
        # 初始化session
        await self.create_session(session_id)
        # 运行agent
        prompt = query['prompt']
        resp_list = await self._run_agent_single_turn(prompt, session_id)

        output_list = []
        for resp in resp_list:
            output_list.append(
                resp.model_dump()
            )
        return output_list


class ClipProcessorFactory(BaseProcessorFactory):
    @classmethod
    def create_processor(cls, **kwargs) -> ClipProcessor:
        session_service = kwargs.get("session_service", InMemorySessionService())
        memory_service = None       # this clip processor does not need memory service
        stream = kwargs.get("stream", False)
        tools = [kwargs.get("tools", get_video_editor_tools())]     # list

        return ClipProcessor(
            session_service=session_service,
            memory_service=memory_service,
            stream=stream,
            tools=tools
        )