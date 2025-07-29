import os
import shutil
from typing import Optional, Callable


from processor.base.processor import BaseProcessor, BaseProcessorFactory
from processor.processor_type import ProcessorName, ProcessorType
from utils.log_config import get_logger
logger = get_logger()


class RemoveProcessor(BaseProcessor):

    def __init__(self):
        super().__init__(
            processor_name=ProcessorName.REMOVE,
            processor_type=ProcessorType.WORKFLOW,
            session_service=None,
            memory_service=None,
            stream=False,
        )

    async def run(self, query: dict, **kwargs) ->list[dict]:
        # 删除query里面的元素
        output_list = []
        remove_queue = query['remove_queue']
        KB_DIR = os.getenv("KB_BASE_PATH")
        for folder_path in remove_queue:
            _folder_path = os.path.join(KB_DIR, folder_path)
            try:
                if os.path.exists(_folder_path):
                    shutil.rmtree(_folder_path)
            except Exception as e:
                    output_list.append({'folder_path': _folder_path, 'status': 'failed', 'error': str(e)})
            pass
        return output_list


class RemoveProcessorFactory(BaseProcessorFactory):
    @classmethod
    def create_processor(cls, **kwargs) -> RemoveProcessor:
        return RemoveProcessor()
