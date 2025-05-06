import os
import shutil
from log_config import get_logger
logger = get_logger()


class RemoveProcessor:

    def __init__(self):
        pass

    def run(self, query:dict) ->list:
        # 删除query里面的元素
        fail_list = []
        remove_queue = query['remove_queue']
        KB_DIR = os.getenv("KB_BASE_PATH")
        for folder_path in remove_queue:
            _folder_path = os.path.join(KB_DIR, folder_path)
            try:
                if os.path.exists(_folder_path):
                    shutil.rmtree(_folder_path)
            except Exception as e:
                    fail_list.append(_folder_path)
            pass
        return fail_list
