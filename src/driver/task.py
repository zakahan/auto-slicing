import queue
import threading
from typing import Callable, Any

from processor.processor_type import ProcessorName


class Task:
    def __init__(
            self,
            processor_name: ProcessorName,
            data: Any

    ):
        self.processor_name = processor_name
        self.data = data

# task队列
asr_queue = queue.Queue()
clip_queue = queue.Queue()
analysis_queue = queue.Queue()
remove_queue = queue.Queue()


# 2. 事件处理器注册机制（核心：通过事件类型映射到处理器）
event_handlers = {}

def register_handler(processor_name: ProcessorName, handler: Callable):
    """注册事件处理器，当特定类型事件发生时调用"""
    if processor_name not in event_handlers:
        event_handlers[processor_name] = []
    event_handlers[processor_name].append(handler)

def publish_task(task: Task):
    """发布事件，触发所有注册的处理器"""
    print(f"发布事件: {task.processor_name}")
    if task.processor_name in event_handlers:
        for handler in event_handlers[task.processor_name]:
            handler(task.data)
