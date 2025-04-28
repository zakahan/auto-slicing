import os
from abc import ABC,abstractmethod

class Parser(ABC):
    def __init__(self):
        # 切片存储路径
        self.kb_raw_path = os.getenv("KB_RAW_PATH")
        self.kb_tmp_path = os.getenv("KB_TMP_PATH")

    @abstractmethod
    def asr2str(self, input_audio: str, language:str = 'auto') -> str:
        ...

    @abstractmethod
    def asr2dict(self, input_audio: str, language:str='auto') -> dict:
        ...

    @abstractmethod
    def batch_asr(self, input_audio: str, language: str='auto') ->list[dict]:
        ...