import os.path as op
from dotenv import load_dotenv
load_dotenv(op.join(op.dirname(op.dirname(__file__)), ".env"))

import os
import shutil
import sys
from pathlib import Path
from loguru import logger
from mcp.server.fastmcp import FastMCP
import subprocess

CONFIG_MODULE_DIR = Path(__file__).parent.resolve()
# 获取配置项目
BAN_LOGGER = os.getenv("MCP_BAN_LOGGER") if os.getenv("MCP_BAN_LOGGER") else False  # 禁止日志输出
LOGGER_FILE_DIR = os.getenv("MCP_LOGGER_FILE_DIR") if os.getenv("MCP_LOGGER_FILE_DIR") is not None else "."
LOGGER_LEVEL = os.getenv("MCP_LOGGER_LEVEL") if os.getenv("MCP_LOGGER_LEVEL") is not None else "DEBUG"
# 视频保存位置
KB_DIR = os.getenv("KB_BASE_PATH") if os.getenv("KB_BASE_PATH") is not None else "./kb"
KB_CLIP = "clip"
KB_MERGE = "merge"
KB_RESULT = "result"

# 设计文件格式如下
# kb/raw 存储原始文件
# kb/clip  存储clip_video处理后的文件 
# kb/merge 存储merge_video处理后的文件
# kb/result 存储工程结束之后的文件，用于后续上传处理

def get_logger():
    if BAN_LOGGER:
        # 移除所有处理器
        logger.remove()
        return logger
    
    if not os.path.exists(os.path.abspath(LOGGER_FILE_DIR)):
        # 如果不存在，那就报错
        raise Exception(f"the logger path is not exists: {os.path.abspath(LOGGER_FILE_DIR)}")
    
    if LOGGER_LEVEL not in {"DEBUG", "INFO", "ERROR", "WARNING"}:
        raise Exception(f"the logger level is not exists: {LOGGER_LEVEL}")
    
    log_path = os.path.join(LOGGER_FILE_DIR, 'logs', 'mcp.log')    
    logger.add(log_path, rotation="500 MB", retention="10 days", level=LOGGER_LEVEL,
               format="{time} | {level} | " + "__VEDIO_EDITOR_SERVER__" + ":{function}:{line} - {message}")
    return logger

# 获取logger
logger = get_logger()

# Define MCP Server
mcp = FastMCP(
    name="VideoEditor",
    description="super video editor by ffmpeg.",
    version="0.1.42"
)

# ----------------------------------------------------
"""
    其实无非就是那么几个事情
    # 视频角度
    clip_video：从原视频中切分出一小块
    merge_videos: 将多个视频按序合并
    # 画面角度
    调色：调整视频的色彩（我觉得我暂时用不到）

    # 内容角度
    添加字幕（这个待开发）
    
"""

# 实际处理
def clip_video(
        original_video_path: str,
        save_folder: str,
        start_time: int,
        stop_time: int,
        title: str,
) -> tuple[bool, str, str]:
    """
    剪切视频并保存到指定文件夹
    :param original_video_path: 原视频文件的路径
    :param save_folder: 保存剪切后视频的文件夹路径
    :param start_time: 开始剪切的时间
    :param stop_time: 结束剪切的时间
    :return: 元组，第一个元素为布尔值表示是否成功，第二个值表示输出位置，第三个元素为日志信息
    """
    logger.debug("-------------------------------------------------")
    logger.debug("参数检查<clip_video>")
    logger.debug(f"origin_video_path: {original_video_path}")
    logger.debug(f"save_folder: {save_folder}")
    logger.debug(f"start_time: {start_time}")
    logger.debug(f"stop_time: {stop_time}")
    logger.debug("-------------------------------------------------")

    # 检查原视频文件是否存在
    if not os.path.isfile(original_video_path):
        error_msg = f"错误：原视频文件不存在。"
        logger.error(error_msg)
        return False, "", error_msg
    
    _, file_extension = os.path.splitext(original_video_path)

    # 检查目标文件夹是否存在，如果不存在则创建
    if not os.path.exists(save_folder):
        try:
            os.makedirs(save_folder)
        except OSError as e:
            error_msg = f"错误：无法创建文件夹，错误信息：{e}"
            logger.error(error_msg)
            return False, "", error_msg

    # 生成输出文件路径
    output_path = os.path.join(save_folder, f"{title}{file_extension}")

    try:
        # 构建 FFmpeg 命令
        command = [
            'ffmpeg',
            '-y',
            '-ss', str(start_time),
            '-to', str(stop_time),
            '-i', original_video_path,
            '-c', 'copy',
            output_path
        ]
        # 执行 FFmpeg 命令
        subprocess.run(command, check=True)
        success_msg = f"视频剪切成功，保存"
        logger.info(success_msg)
        return True, output_path, success_msg
    except subprocess.CalledProcessError as e:
        error_msg = f"错误：执行 FFmpeg 命令时出错，错误信息：{e}"
        logger.error(error_msg)
        return False, "", error_msg


def merge_videos(video_paths: list[str], save_folder:str) -> tuple[bool, str, str]:
    """
    合并多个本地视频文件
    :param video_paths: 包含视频文件路径的列表
    :return: 元组，第一个元素为布尔值表示是否成功，第二个元素为日志信息
    """
    logger.debug("-------------------------------------------------")
    logger.debug("参数检查<merge_video>")
    logger.debug(f"video_path: {str(video_paths)}")
    logger.debug(f"save_folder: {save_folder}")
    logger.debug("-------------------------------------------------")
    # 检查所有视频文件是否存在
    for path in video_paths:
        if not os.path.isfile(path):
            error_msg = f"错误：视频文件不存在。"
            logger.error(error_msg)
            return False, "",  error_msg

    # 检查目标文件夹是否存在，如果不存在则创建
    if not os.path.exists(save_folder):
        try:
            os.makedirs(save_folder)
        except OSError as e:
            error_msg = f"错误：无法创建文件夹，错误信息：{e}"
            logger.error(error_msg)
            return False, "", error_msg



    # 创建临时文件列表
    temp_file_list = 'temp_file_list.txt'
    try:
        with open(temp_file_list, 'w', encoding='utf-8') as f:
            for path in video_paths:
                f.write(f"file '{path}'\n")

        # 生成输出文件路径
        output_path = os.path.join(save_folder, f'result.mp4')

        # 构建 FFmpeg 命令
        command = [
            'ffmpeg',
            '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', temp_file_list,
            '-c', 'copy',
            output_path
        ]
        # 执行 FFmpeg 命令
        subprocess.run(command, check=True)
        success_msg = f"视频合并成功，成功保存"
        logger.info(success_msg)
        return True, output_path, success_msg
    except subprocess.CalledProcessError as e:
        error_msg = f"错误：执行 FFmpeg 命令时出错，错误信息：{e}"
        logger.error(error_msg)
        return False, "", error_msg
    except Exception as e:
        error_msg = f"发生未知错误：{e}"
        logger.error(error_msg)
        return False, "", error_msg
    finally:
        # 删除临时文件列表
        if os.path.exists(temp_file_list):
            os.remove(temp_file_list)

def copy_file(source_file:str, target_folder:str) -> bool:
    try:
        if not os.path.isfile(source_file):
            return False
        
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        # 移动文件
        shutil.move(source_file, target_folder)
        return True
    except Exception as e:
        return False
        

# --------------------------------------------------------------------------
# mcp-tools注册
@mcp.tool()
def clip_video_tool(
        original_video_path: str,
        task_id: str,
        start_time: int,
        stop_time: int,
        title: str,
) -> dict:
    """
    Clip a video based on the given start and stop times.
    
    Parameters:
    original_video_path (str): The path of the original video file relative to the KB_DIR.
    task_id (str): The unique identifier for the clipping task.
    start_time (int): The start time (in some appropriate unit) for the clipping.
    stop_time (int): The stop time (in some appropriate unit) for the clipping.
    task_id (str): title: the title of the clipping.
    Returns:
    dict: A dictionary containing the result of the clipping operation.
          The dictionary has the following keys:
          - "success": A boolean indicating whether the operation was successful.
          - "message": A string providing additional information about the operation.
          - "output_path": The path of the clipped video file relative to the KB_DIR.
    """
    # 要保证，每次输入都是基于KB的，每次输出也都是基于KB的
    _original_video_path = os.path.join(KB_DIR, original_video_path)
    _save_folder = os.path.join(KB_DIR, KB_CLIP, task_id)
    success, output_path, message = clip_video(
        _original_video_path, _save_folder, start_time, stop_time, title)
    return {"success": success, "message": message, "output_path": output_path[len(KB_DIR)+1:]}


@mcp.tool()
def merge_videos_tool(video_paths: list[str], task_id: str) -> dict:
    """
    Merge multiple videos into one.

    Parameters:
    video_paths (list[str]): A list of paths of the video files to be merged, relative to the KB_DIR.
    task_id (str): The unique identifier for the merging task.

    Returns:
    dict: A dictionary containing the result of the merging operation.
          The dictionary has the following keys:
          - "success": A boolean indicating whether the operation was successful.
          - "message": A string providing additional information about the operation.
          - "output_path": The path of the merged video file relative to the KB_DIR.
    """
    _video_paths = []
    for path in video_paths:
        _video_paths.append(os.path.join(KB_DIR, path))
        pass
    _save_folder = os.path.join(KB_DIR, KB_MERGE, task_id)
    success, output_path, message = merge_videos(_video_paths, _save_folder)

    return {"success": success, "message": message, "output_path": output_path[len(KB_DIR)+1:]}


@mcp.tool()
def move_videos_tools(video_path: str, task_id: str) -> dict:
    _video_path = os.path.join(KB_DIR, video_path)
    _target_folder = os.pardir.join(KB_DIR, KB_RESULT, task_id)
    if copy_file(source_file=_video_path, target_folder=_target_folder):
        return {
            "success": True
        }
    else:
        return {
            "success": False
        }
    
    


if __name__ == "__main__":
    logger.info("Video Editor MCP Server Running......")
    mcp.run(transport='stdio')