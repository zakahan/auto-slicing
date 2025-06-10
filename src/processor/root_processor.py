import os
from .asr_processor import ASRProcessor
from .analysis_processor import AnalysisProcessor
from .clip_processor import ClipProcessor
from .subtitles_processor import SubtitlesProcessor
from .remove_processor import RemoveProcessor
from parser.json_parser import jsonl_fuzzy_parser
import glob
from log_config import get_logger

logger = get_logger()


def find_video_files(directory: str, task_id: str) -> list[dict[str, str]]:
    video_extensions = ('.mp4', '.avi', '.mov')
    video_files: list[dict[str, str]] = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(video_extensions):
                # file_path = os.path.join(root, file)
                video_files.append(
                    {
                        "task_id": task_id, "title": file,  # "path": file_path,
                    })
    return video_files


class RootProcessor:
    def __init__(self, is_create_subtitles: bool = False, prompt_key: str = 'easy'):
        self.is_create_subtitles = is_create_subtitles
        self.prompt_key = prompt_key
        pass

    def _get_video_path(self, task_id_list: list[str]) -> list[dict]:
        res_list = []
        for task_id in task_id_list:
            dir_path = os.path.join(os.getenv("KB_BASE_PATH"), "result", task_id)
            v_list = find_video_files(dir_path, task_id)

            res_list.extend(v_list)
        return res_list

    async def run(self, query: dict) -> list[dict]:
        task_id_list = []
        task_id = query['task_id']
        raw_video = query['raw_video']
        introduction = query['introduction']
        # task_id: str, raw_video: str, introduction: str
        # 语音识别阶段 ---------------------------------------------------------
        asr_pcr = ASRProcessor()
        asr_task_id = f"{task_id}_asr"
        asr_results = asr_pcr.run(
            query={
                "input_audio": raw_video,
                "task_id": asr_task_id
            }
        )

        # 分析阶段 ---------------------------------------------------------
        aly_pcr = AnalysisProcessor()
        aly_results = []        # list[str]
        for i in range(len(asr_results['batch'])):
            aly = await aly_pcr.run(        # str
                query={
                    'content': str(asr_results['batch'][i]),
                    'introduction': introduction
                },
                prompt_key=self.prompt_key
            )
            aly_results.append(aly)
            pass

        # 切片阶段 -----------------------------------------------------------
        clp_prc = ClipProcessor()
        prompt_clp_task_query = []      # 这里是分歧点

        for aly_res in aly_results:
            try:
                prompt_clp_task_query.extend(jsonl_fuzzy_parser(aly_res))
            except Exception as e:
                logger.error("json_repair error" + str(e))

        for i, query in enumerate(prompt_clp_task_query):
            if not all(key in query for key in ('start_time', 'stop_time', 'title')):
                logger.error(f"clp_task阶段：本次有字段缺失问题，{query.keys()}")
                break
            task_id = f"{task_id}_{i}"
            task_id_list.append(f"{task_id}_{i}")
            clp = await clp_prc.run(
                query, raw_video, task_id, prompt_key=self.prompt_key
            )
            logger.info(f"{task_id}_{i}: {clp}")
            pass

        rme_prc = RemoveProcessor()
        rme_prc.run({
            'remove_queue': [
                'slice',
                'clip'
            ]
        })

        return self._get_video_path(task_id_list)

