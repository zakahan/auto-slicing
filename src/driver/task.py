import queue
import threading
from typing import Callable, Any

from processor.processor_type import ProcessorType


class Task:
    def __init__(
            self,
            processor_type: ProcessorType,
            data: Any

    ):
        self.processor_type = processor_type
        self.data = data

# task队列
asr_queue = queue.Queue()
clip_queue = queue.Queue()
analysis_queue = queue.Queue()
remove_queue = queue.Queue()


# 2. 事件处理器注册机制（核心：通过事件类型映射到处理器）
event_handlers = {}

def register_handler(processor_type: ProcessorType, handler: Callable):
    """注册事件处理器，当特定类型事件发生时调用"""
    if processor_type not in event_handlers:
        event_handlers[processor_type] = []
    event_handlers[processor_type].append(handler)

def publish_task(task: Task):
    """发布事件，触发所有注册的处理器"""
    print(f"发布事件: {task.processor_type}")
    if task.processor_type in event_handlers:
        for handler in event_handlers[task.processor_type]:
            handler(task.data)
