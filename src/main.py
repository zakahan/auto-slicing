import asyncio
import os
from dotenv import load_dotenv
# 加载.env文件中的环境变量
load_dotenv()

from parser.json_parser import json2dict
from processor.root_processor import RootProcessor


introduction= json2dict("introduction.json")

query = {
        "task_id":"007",
        "raw_video":"raw/【直播回放】不动如山 2025年01月06日20点场.mp4",
        "introduction":introduction["雫るる_Official"]
}


root_pcr = RootProcessor()

x= asyncio.run(
    root_pcr.run(
        query=query
    )
)


for item in x:
    print(item)