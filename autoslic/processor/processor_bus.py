from autoslic.processor_factory import ProcessorFactory
from autoslic.processor_type import ProcessorName

class ProcessorBus:
    def __init__(self):
        processor_keys = ProcessorName.get_attr()
        self.processors = {}
        for key in processor_keys:
            self.processors[key] = ProcessorFactory.create_processor(processor_name=key)
        pass

    def process(self, data: dict):
        processor_chain = data['processor_chain']
        queries = data['query']
        for processor_name in processor_chain:
            processor = self.processors[processor_name]
            output = processor.run(queries=queries)
            queries = processor.post_process(output)

        # 结束后返回结果