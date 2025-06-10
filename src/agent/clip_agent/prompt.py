from utils.workflow_type import WorkflowType

AGENT_DESCRIPTION = """
你是一个视频剪辑专家，你现在要做这样的一个任务：
现在有一整段视频，来自于一名主播的直播录像，你要担任视频切片员，根据提供的切片指令要求进行切分。
这边会提供给你视频剪辑的工具，你调用即可。
"""

AGENT_INSTRUCTION = """
你需要执行剪辑操作，我会提供给你多个参数，包括剪切起始时间与剪切终止时间以及文件位置、文件保存位置等，你需要操纵工具将视频裁剪出来。
你无需担心剪辑后视频的存储位置，至于输入的文件位置，你只需要输入相对路径即可。
"""


def get_clip_prompt(query: dict, origin_video_path: str, task_id: str, key: str) -> str:
    match key:
        case WorkflowType.EASY:
            prompt = (
                f"你需要对一段视频执行剪辑操作，要求如下\n"
                f"在原素材上切分出一段视频，随后修改标题，要求全过程都使用工具完成。\n"
                f"参数如下：\n"
                f"1. origin_video_path: {origin_video_path}：\n"
                f"2. task_id: {task_id}\n"
                f"3. start_time:{query['start_time']}\n"
                f"4. stop_time:{query['stop_time']}\n"
                f"5. title: {query['title']} \n"
                f"请完成剪辑任务，注意，每次任务结束后，都要调用任务结束对应的工具。"
            )
        case WorkflowType.WITH_START:
            prompt = (
                f"你需要对一段视频执行剪辑操作，要求如下\n"
                f"一共两次操作\n"
                f"### 第一次操作:"
                f"在原素材上切分出一段视频，随后修改标题，要求全过程都使用工具完成。\n"
                f"参数如下：\n"
                f"1. origin_video_path: {origin_video_path}：\n"
                f"2. task_id: {task_id}\n"
                f"3. start_time:{query['start_time']}\n"
                f"4. stop_time:{query['stop_time']}\n"
                f"5. title: {query['title']} \n"
                f"### 第二次操作\n"
                f"对刚刚剪切好的视频添加片头，片头的地址如下:\n"
                f"sequence_video_path: {query['sequence_video_path']}\n"
                f"请完成剪辑任务，注意，每次任务结束后，都要调用任务结束对应的工具。"
            )
        case WorkflowType.TWO_STEP:
            prompt = (
                f"你需要对一段视频执行剪辑操作，要求如下\n"
                f"先在原素材上切分出两段视频，随后按顺序合并。\n"
                f"参数如下：\n"
                f"1. origin_video_path: {origin_video_path}：\n"
                f"2. 第一段视频\n"
                f"    2.1 task_id: {query['clip'][0]['task_id']}\n"
                f"    2.2. start_time:{query['clip'][0]['start_time']}\n"
                f"    2.3. stop_time:{query['clip'][0]['stop_time']}\n"
                f"3. 第二段视频\n"
                f"    3.1 task_id: {query['clip'][1]['task_id']}\n"
                f"    3.2 start_time:{query['clip'][1]['start_time']}\n"
                f"    3.3 stop_time:{query['clip'][1]['stop_time']}\n"
                f"4. 合并两段视频\n"
                f"    4.1 task_id: {query['merge']['task_id']},\n"
                f"    4.2 video_paths: 请你根据前两段视频合并操作的结果来决定\n"
                f"5. 将视频重命名为\n"
                f"请完成剪辑任务\n"
            )
        case _:
            raise KeyError(f"Please set a usable key. I don't know what this '{key}' you found is.")

    return prompt
