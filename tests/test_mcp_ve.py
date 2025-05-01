import os
import os.path as op
from dotenv import load_dotenv
load_dotenv(op.join(op.dirname(op.dirname(__file__)), "src/.env"))

from mcp_servers.video_editor_server import clip_video, clip_video_tool
from mcp_servers.video_editor_server import merge_videos, merge_videos_tool


print(os.getenv("KB_RAW_PATH"))

# res = clip_video(
#     original_video_path="/home/hanzhi/contents/auto_slicing/kb/raw/test.mp4",
#     save_folder="/home/hanzhi/contents/auto_slicing/kb/tmp/cut/003",
#     start_time=22,
#     stop_time=31,

# )



# 测试合并功能

# res = merge_videos(
#     video_paths=[
#         "/home/hanzhi/contents/auto_slicing/kb/tmp/cut/001/cut_test.mp4",
#         "/home/hanzhi/contents/auto_slicing/kb/tmp/cut/002/cut_test.mp4",
#     ],
#     save_folder="/home/hanzhi/contents/auto_slicing/kb/tmp/merge",

# )

# print(res)


# res = clip_video_tool(
#     original_video_path="raw/test.mp4",
#     task_id="005",
#     start_time=22,
#     stop_time=33
# )
# print(res)

res = merge_videos_tool(
    video_paths=[
        "clip/005/result.mp4",
        "clip/005/result.mp4"
    ],
    task_id="008"
)
print(res)