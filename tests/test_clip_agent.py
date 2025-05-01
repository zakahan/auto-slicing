import os
import os.path as op
from dotenv import load_dotenv
load_dotenv(op.join(op.dirname(op.dirname(__file__)), "src/.env"))

import asyncio
from processor.clip_processor import ClipProcessor

clip_processor = ClipProcessor()


query = {
    "origin_video_path": "raw/test.mp4",
    "clip": [
        {
            "task_id": "001",
            "start_time": 10,
            "stop_time": 20,
        },
        {
            "task_id": "002",
            "start_time": 10,
            "stop_time": 20,
        }
    ],
    "merge": {
        "task_id": "003",
    }

}

x = asyncio.run(clip_processor.run(query))

print(x)