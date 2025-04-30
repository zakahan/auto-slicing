import os
import sys
from pathlib import Path
from loguru import logger
from mcp.server.fastmcp import FastMCP
import subprocess

CONFIG_MODULE_DIR = Path(__file__).parent.resolve()
# 获取配置项目
LOGGER_FILE_DIR = os.getenv("MCP_LOGGER_FILE_DIR") if os.getenv("MCP_LOGGER_FILE_DIR") is not None else "."
LOGGER_LEVEL = os.getenv("MCP_LOGGER_LEVEL") if os.getenv("MCP_LOGGER_LEVEL") is not None else "INFO"
# 视频保存位置
SVAE_DIR=""
ORIGIN_VIDEO_DIR=""


def get_logger():
    # log_path = 
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

# 实际实现


def cut_video(original_video_path: str, save_folder: str, start_time: int, stop_time: int) -> tuple[bool, str]:
    """
    剪切视频并保存到指定文件夹
    :param original_video_path: 原视频文件的路径
    :param save_folder: 保存剪切后视频的文件夹路径
    :param start_time: 开始剪切的时间
    :param stop_time: 结束剪切的时间
    :return: 元组，第一个元素为布尔值表示是否成功，第二个元素为日志信息
    """
    # 检查原视频文件是否存在
    if not os.path.isfile(original_video_path):
        error_msg = f"错误：原视频文件 {original_video_path} 不存在。"
        logger.error(error_msg)
        return False, error_msg

    # 检查目标文件夹是否存在，如果不存在则创建
    if not os.path.exists(save_folder):
        try:
            os.makedirs(save_folder)
        except OSError as e:
            error_msg = f"错误：无法创建文件夹 {save_folder}，错误信息：{e}"
            logger.error(error_msg)
            return False, error_msg

    # 生成输出文件路径
    video_name = os.path.basename(original_video_path)
    output_path = os.path.join(save_folder, f"cut_{video_name}")

    try:
        # 构建 FFmpeg 命令
        command = [
            'ffmpeg',
            '-ss', str(start_time),
            '-to', str(stop_time),
            '-i', original_video_path,
            '-c', 'copy',
            output_path
        ]
        # 执行 FFmpeg 命令
        subprocess.run(command, check=True)
        success_msg = f"视频剪切成功，保存到 {output_path}"
        logger.info(success_msg)
        return True, success_msg
    except subprocess.CalledProcessError as e:
        error_msg = f"错误：执行 FFmpeg 命令时出错，错误信息：{e}"
        logger.error(error_msg)
        return False, error_msg


def merge_videos(video_paths: list[str]) -> tuple[bool, str]:
    """
    合并多个本地视频文件
    :param video_paths: 包含视频文件路径的列表
    :return: 元组，第一个元素为布尔值表示是否成功，第二个元素为日志信息
    """
    # 检查所有视频文件是否存在
    for path in video_paths:
        if not os.path.isfile(path):
            error_msg = f"错误：视频文件 {path} 不存在。"
            logger.error(error_msg)
            return False, error_msg

    # 创建临时文件列表
    temp_file_list = 'temp_file_list.txt'
    try:
        with open(temp_file_list, 'w', encoding='utf-8') as f:
            for path in video_paths:
                f.write(f"file '{path}'\n")

        # 生成输出文件路径
        output_path = 'merged_video.mp4'

        # 构建 FFmpeg 命令
        command = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', temp_file_list,
            '-c', 'copy',
            output_path
        ]
        # 执行 FFmpeg 命令
        subprocess.run(command, check=True)
        success_msg = f"视频合并成功，保存到 {output_path}"
        logger.info(success_msg)
        return True, success_msg
    except subprocess.CalledProcessError as e:
        error_msg = f"错误：执行 FFmpeg 命令时出错，错误信息：{e}"
        logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"发生未知错误：{e}"
        logger.error(error_msg)
        return False, error_msg
    finally:
        # 删除临时文件列表
        if os.path.exists(temp_file_list):
            os.remove(temp_file_list)


if __name__ == "__main__":
    logger = get_logger()
    logger.debug("test 1")
    logger.info("test 2")