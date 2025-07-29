import asyncio
import os
import secrets
from dotenv import load_dotenv
# 加载.env文件中的环境变量
load_dotenv()

from parser.json_parser import json2dict
from processor.event_driven_processor import EventDrivenProcessor


introduction= json2dict("introduction.json")

query = {
        "task_id":secrets.token_hex(4),
        "raw_video":"raw/test.mp4",
        "introduction":introduction["雫るる_Official"]
}


event_driven_processor = EventDrivenProcessor()

x= asyncio.run(
    event_driven_processor.run(
        query=query
    )
)


for item in x:
    print(item)