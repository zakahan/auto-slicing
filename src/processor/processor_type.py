from enum import StrEnum


class ProcessorName(StrEnum):
    BASE = "base"
    CLIP = "clip"
    ANALYSIS = "analysis"
    ASR = "asr"
    SUBTITLE = "subtitle"
    REMOVE = "remove"
    ROOT = "root"


class ProcessorType(StrEnum):
    WORKFLOW = "workflow"
    AGENTIC = "agentic"


class WorkflowType(StrEnum):
    EASY = 'easy'
    WITH_START= 'with_start'
    TWO_STEP = 'two_step'
