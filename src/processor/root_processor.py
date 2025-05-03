from .asr_processor import ASRProcessor
from .analysis_processor import AnalysisProcessor
from .clip_processor import ClipProcessor
from .subtitles_processor import SubtitlesProcessor
from parser.json_parser import jsonl_parser
from log_config import get_logger
logger = get_logger()


class RootProcessor:
    def __init__(self, is_create_subtitles=False):
        self.is_create_subtitles = is_create_subtitles
        pass

    async def run(self, task_id: str, raw_video: str, introduction: str):
        # 开始！

        # ---------------------------------------------------------
        asr_pcr = ASRProcessor()
        asr_task_id = f"{task_id}_asr"
        asr_results = asr_pcr.run(
            query={
                "input_audio": raw_video,
                "task_id": asr_task_id
        })
        # ---------------------------------------------------------
        # 创建字幕文件
        if self.is_create_subtitles:
            srt_prc = SubtitlesProcessor()
            srt_success, srt_file_path = srt_prc.run(
                query={
                    "task_id": f"{task_id}",
                    "asr_list": asr_results['asr']
                }
            )

        # ---------------------------------------------------------
        aly_pcr = AnalysisProcessor()
        aly_task_id_group = [f"{task_id}_aly_{i}" for i in range(len(asr_results['batch']))]
        aly_results = []
        for i, aly_task_id in enumerate(aly_task_id_group):
            aly = await aly_pcr.run(asr_results['batch'][i], introduction)
            aly_results.append(aly)
            pass

        # -----------------------------------------------------------
        # 切片  
        # 这里再添加一步，根据srt_success和is_create_subtitles，来判断使用哪个run
        clp_prc = ClipProcessor()
        prompt_clp_task_query = []

        for aly_res in aly_results:
            try:
                prompt_clp_task_query.extend(jsonl_parser(aly_res))
            except Exception as e:
                logger.error("json_repair error"+str(e))

        for i, clp_task in enumerate(prompt_clp_task_query):
            if not all(key in clp_task for key in ('start_time', 'stop_time', 'title')):
                # 缺了字段就跳过，并且记录
                logger.error(f"clp_task阶段：本次有字段缺失问题，{clp_task.keys()}")
                break
            query = {
                "origin_video_path": raw_video,
                "task_id": f"{task_id}_{i}",
                "start_time": clp_task["start_time"],
                "stop_time": clp_task["stop_time"],
                "title": clp_task['title']
            }
            clp = await clp_prc.run(query)
            logger.info(f"{task_id}_{i}: {clp}")
            if i > 15:
                break
            pass


        return 'success'
