
import os
from loguru import logger
from pathlib import Path

CONFIG_MODULE_DIR = Path(__file__).parent.resolve()

os.environ["LOGURU_LEVEL"] = "INFO"

def get_logger(module_name:str, file_name="app.log"):
    log_path = os.path.join(os.path.dirname(CONFIG_MODULE_DIR), "logs", file_name)
    logger.add(log_path, rotation="500 MB", retention="10 days",# level="INFO",
               format="{time} | {level} | " + module_name + ":{function}:{line} - {message}")
    return logger


if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("test 1")
    logger.info("test 2")