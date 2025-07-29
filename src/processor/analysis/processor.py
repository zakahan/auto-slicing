import uuid
from typing import Optional, Callable

from google.adk.memory import BaseMemoryService
from google.adk.sessions import InMemorySessionService, BaseSessionService
from google.adk.tools.base_toolset import BaseToolset

from agent_kit.agent_factory import create_agent
from processor.base.processor import BaseProcessor, BaseProcessorFactory
from processor.analysis.prompt import AGENT_DESCRIPTION, AGENT_INSTRUCTION
from processor.processor_type import ProcessorName, ProcessorType
from utils.log_config import get_logger

logger = get_logger()

class AnalysisProcessor(BaseProcessor):
    def __init__(
            self,
            session_service: Optional[BaseSessionService] = None,
            memory_service: Optional[BaseMemoryService] = None,
            stream: bool = False,

    ):
        super().__init__(
            processor_name=ProcessorName.ANALYSIS,
            processor_type=ProcessorType.AGENTIC,
            session_service=session_service,
            memory_service=memory_service,
            stream=stream,
        )
        self.agent = create_agent(
            agent_name=self._app_name,
            agent_description=AGENT_DESCRIPTION,
            agent_instruction=AGENT_INSTRUCTION,
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


class AnalysisProcessorFactory(BaseProcessorFactory):
    @classmethod
    def create_processor(cls, **kwargs) -> AnalysisProcessor:
        session_service = kwargs.get("session_service", InMemorySessionService())
        memory_service = None       # this clip processor does not need memory service
        stream = False

        return AnalysisProcessor(
            session_service=session_service,
            memory_service=memory_service,
            stream=stream,
        )