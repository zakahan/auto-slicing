import os

from parser.asr.sv_local_parser import SVLocalParser
from log_config import get_logger
logger = get_logger()



class ASRProcessor:
    def __init__(self):
        self.app_name = "asr_app"
        if os.getenv("ASR_BATCH_MAX_WINDOWS_SIZE") is None:
            self.max_windows_size = 5000  # 按这个数量切割task
        else:
            self.max_windows_size = int(os.getenv("ASR_BATCH_MAX_WINDOWS_SIZE"))
        # 其实我感觉还得加个chunk_overlap的......
        # 没啥要保存的


    def run(self, query: dict) -> dict:
        # 输入路径也要是基于KB的
        sv_parser = SVLocalParser()
        input_audio_path = os.path.join(sv_parser.kb_dir_path, query["input_audio"])
        slice_list = sv_parser.asr2dict(
            input_audio=input_audio_path,       # 这里是绝对路径，不同于那几个mcp
            task_id=query["task_id"]
        )
        result = {}
        result['batch'] = []
        result['asr'] = slice_list
        p = []
        total_length = 0
        for slice in slice_list:

            if total_length >= self.max_windows_size:
                result['batch'].append(p)
                p = []      # 分批防止超出上下文窗口
                total_length = 0

            total_length += len(slice['text'])
            # 添加到结果dict
            p.append(
                {
                    "start_time": slice['start_time'],
                    "stop_time": slice['stop_time'],
                    "text": slice['text']
                }
            )
            pass

        # 结束之后补上
        result['batch'].append(p)
        return result
