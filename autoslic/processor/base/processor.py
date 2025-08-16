import uuid
from abc import abstractmethod, ABC
from typing import Optional

from google.adk.events import Event
from google.adk.memory import BaseMemoryService
from google.adk.sessions import BaseSessionService

from autoslic.agent_kit.run_agent import run_by_single_turn
from autoslic.agent_kit.dto import RunResponse
from autoslic.processor.processor_type import ProcessorName, ProcessorType


class BaseProcessor(ABC):
    def __init__(
        self,
        processor_name: str = ProcessorName.BASE,
        processor_type: str = ProcessorType.WORKFLOW,
        session_service: Optional[BaseSessionService] = None,
        memory_service: Optional[BaseMemoryService] = None,
        stream: bool = False,
    ):
        # basic info
        self._app_name = processor_name
        self._user_id = "user_01"

        # runner config
        self.processor_type = processor_type
        if processor_type == ProcessorType.WORKFLOW:
            from google.adk.agents import RunConfig
            from google.adk.agents.run_config import StreamingMode

            self._run_config = RunConfig(
                streaming_mode=StreamingMode.NONE if not stream else StreamingMode.SSE,
            )
        else:
            self._run_config = None

        # services
        self.session_service = session_service
        self.memory_service = memory_service

        # agent
        self.agent = None

    @property
    def processor_name(self) -> str:
        return self._app_name

    @abstractmethod
    async def run(self, queries: list[dict], **kwargs) -> list[dict]:
        raise NotImplementedError


    async def _run_agent_single_turn(self, prompt: str, **kwargs) -> list[RunResponse]:
        assert self.processor_type == ProcessorType.AGENTIC, "only agentic processor can run agent"
        assert self.session_service, "session_service is required"
        assert self.agent, "agent is required"
        from google.adk.runners import Runner

        session_id = str(uuid.uuid4())  # generate a session id
        # 初始化session
        await self.create_session(session_id)
        # 运行agent
        runner = Runner(
            app_name=self._app_name,
            agent=self.agent,
            session_service=self.session_service,
            memory_service=self.memory_service,
        )

        return await run_by_single_turn(
            runner=runner,
            prompt=prompt,
            run_config=self._run_config,
            user_id=self._user_id,
            session_id=session_id,
        )


    async def create_session(self, session_id: str) -> bool:
        if self.session_service:
            await self.session_service.create_session(
                app_name=self._app_name,
                user_id=self._user_id,
                session_id=session_id,
            )
            return True
        else:
            return False

    async def add_event_to_session(self, session_id: str, events: list[Event]):
        if self.session_service:
            session = await self.session_service.get_session(
                app_name=self._app_name,
                user_id=self._user_id,
                session_id=session_id,
            )
            if not session:
                raise ValueError(f"Session {session_id} not found")
            for event in events:
                await self.session_service.append_event(session, event)

    def post_process(self, result: list[dict]) -> list[dict]:
        # 1. 检查结果是否格式规范
        # 2. 检查结果是否符合预期
        return result


class BaseProcessorFactory(ABC):
    @classmethod
    def create_processor(cls, **kwargs) -> BaseProcessor:
        raise NotImplementedError
