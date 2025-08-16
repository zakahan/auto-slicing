import os
from abc import ABC,abstractmethod

class Parser(ABC):
    def __init__(self):
        # 切片存储路径
        self.kb_dir_path:str = os.getenv("KB_BASE_PATH")
        self.kb_vad_path = os.path.join(self.kb_dir_path, "slice")

    # @abstractmethod
    # def asr2str(self, input_audio: str, language:str = 'auto') -> str:
    #     ...
    #
    # @abstractmethod
    # def asr2dict(self, input_audio: str, language:str='auto') -> dict:
    #     ...
    #
    # @abstractmethod
    # def batch_asr(self, input_audio: str, language: str='auto') ->list[dict]:
    #     ...