from enum import StrEnum

# must python 3.11 +
class WorkflowType(StrEnum):
    EASY = 'easy'
    WITH_START= 'with_start'
    TWO_STEP = 'two_step'




# doc:
# easy: 常规模式，纯粹的剪辑
# with_start: 片头 + 内容形式
# two_step: 两阶段模式，先把标题内容放前面，然后是全文（这个prompt不知道怎么写）
