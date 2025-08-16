from enum import StrEnum


class ProcessorName(StrEnum):
    BASE = "base"
    CLIP = "clip"
    ANALYSIS = "analysis"
    ASR = "asr"
    SUBTITLE = "subtitle"
    REMOVE = "remove"
    ROOT = "root"

    @classmethod
    def get_attr(cls) -> list[str]:
        return [member.value for member in cls.__members__.values()]

class ProcessorType(StrEnum):
    WORKFLOW = "workflow"
    AGENTIC = "agentic"


class WorkflowType(StrEnum):
    EASY = 'easy'
    WITH_START= 'with_start'
    TWO_STEP = 'two_step'
