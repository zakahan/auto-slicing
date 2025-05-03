import os
from log_config import get_logger
logger = get_logger()


def seconds_to_srt_time(seconds: int):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def generate_srt_subtitle(subtitles, output_file) -> bool:
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for index, (start_sec, end_sec, text) in enumerate(subtitles, start=1):
                start_time = seconds_to_srt_time(start_sec)
                end_time = seconds_to_srt_time(end_sec)
                f.write(f"{index}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
        logger.info(f"SRT 字幕文件已成功生成到 {output_file}")
        return True
    except Exception as e:
        err_msg =  f"生成 SRT 字幕文件时出错: {e}"
        logger.error(err_msg)
        return False


class SubtitlesProcessor:
    def __init__(self):
        # 目前只支持生成srt文件
        self.srt_base_path = os.path.join(os.getenv("KB_BASE_PATH"), "srt")
        pass

    def run(self, query: dict) -> str:
        task_id = query['task_id']
        asr_list = query['asr_list']
        
        # asr_list的格式
        # list[dict]
        # 每个dict：
        # {start_time, stop_time, text}
        srt_item_list = []
        for item in asr_list:
            start_time = item['start_time']
            stop_time = item['stop_time']
            text = item['text']
            srt_item_list.append(
                (start_time, stop_time, text)
            )
            pass
        task_folder = os.path.join(self.srt_base_path, task_id)
        if not os.path.exists(task_folder):
            os.makedirs(task_folder)
        # 生成字幕文件
        output_path = os.path.join(task_folder, "subtitles.srt")
        res = generate_srt_subtitle(srt_item_list, output_path)
        return {"result":res, "output_path": output_path}
    