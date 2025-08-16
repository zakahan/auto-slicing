import uuid
from typing import Optional, Callable

from google.adk.memory import BaseMemoryService
from google.adk.sessions import InMemorySessionService, BaseSessionService
from google.adk.tools.base_toolset import BaseToolset

from autoslic.agent_kit.agent_factory import create_agent
from autoslic.parser.json_parser import jsonl_fuzzy_parser
from autoslic.processor.base.processor import BaseProcessor, BaseProcessorFactory
from autoslic.processor.analysis.prompt import AGENT_DESCRIPTION, AGENT_INSTRUCTION, get_analysis_prompt
from autoslic.processor.processor_type import ProcessorName, ProcessorType
from autoslic.utils.log_config import get_logger

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

    async def run(self, queries: list[dict], **kwargs) -> list[dict]:
        output_list = []

        for query in queries:
            prompt = get_analysis_prompt(query)
            completion = await self._run_agent_single_turn(prompt=prompt, **kwargs)
            try:
                output = jsonl_fuzzy_parser(completion[-1].content.text)
            except Exception as e:
                logger.error(f"analysis processor output is not jsonl format, error: {e}")
                continue

            # add outputs
            if isinstance(output, dict):
                output_list.append(output)
            elif isinstance(output, list):
                output_list.extend(output)
            else:
                logger.info(f"analysis processor output is not dict or list, output: {output}")

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