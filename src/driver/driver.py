import time
from driver.task import (
    Task,
    asr_queue,
    clip_queue,
    analysis_queue,
    remove_queue,
    register_handler,
    publish_task
)
import threading

from processor.processor_type import ProcessorName
from processor.processor_factory import ProcessorFactory

asr_processor = ProcessorFactory.create_processor(ProcessorName.ASR)
clip_processor = ProcessorFactory.create_processor(ProcessorName.CLIP)
analysis_processor = ProcessorFactory.create_processor(ProcessorName.ANALYSIS)
remove_processor = ProcessorFactory.create_processor(ProcessorName.REMOVE)
subtitle_processor = ProcessorFactory.create_processor(ProcessorName.SUBTITLE)


async def asr_processing():
    task = asr_queue.get()
    results = await asr_processor.run(task)
    for result in results:
        # 保证每个run函数返回值都是一个list[dict]，然后队列是对每个dict做处理的
        publish_task(
            Task(
                processor_name=ProcessorName.ASR,
                data=result
            )
        )
    asr_queue.task_done()
    pass