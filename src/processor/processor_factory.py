from processor.analysis.processor import AnalysisProcessor
from processor.asr.processor import ASRProcessor
from processor.clip.processor import ClipProcessor
from processor.processor_type import ProcessorName
from processor.remove.processor import RemoveProcessor
from processor.subtitles.processor import SubtitlesProcessor


class ProcessorFactory:
    @classmethod
    def create_processor(cls, processor_name: ProcessorName,
                         **kwargs: object) -> SubtitlesProcessor | AnalysisProcessor | ClipProcessor | ASRProcessor | RemoveProcessor:
        match processor_name:
            case ProcessorName.CLIP:
                from processor.clip.processor import ClipProcessorFactory
                return ClipProcessorFactory.create_processor(**kwargs)
            case ProcessorName.ANALYSIS:
                from processor.analysis.processor import AnalysisProcessorFactory
                return AnalysisProcessorFactory.create_processor(**kwargs)
            case ProcessorName.ASR:
                from processor.asr.processor import ASRProcessorFactory
                return ASRProcessorFactory.create_processor(**kwargs)
            case ProcessorName.SUBTITLE:
                from processor.subtitles.processor import SubtitlesProcessorFactory
                return SubtitlesProcessorFactory.create_processor(**kwargs)
            case ProcessorName.REMOVE:
                from processor.remove.processor import RemoveProcessorFactory
                return RemoveProcessorFactory.create_processor(**kwargs)
            case _:
                raise ValueError(f"Unsupported processor name: {processor_name}")