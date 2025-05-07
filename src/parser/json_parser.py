import os
import json
import json_repair


# for llm response json type text
def jsonl_fuzzy_parser(text:str) -> list[dict]:
    return json_repair.loads(text)

def json2dict(file_path: str) -> dict:
    return json.load(file_path)

def dict2json(file_path: str) -> bool:
    return json.dump(file_path)




if __name__ == "__main__":
    pass