import os
import json
import json_repair


# for llm response json type text
def jsonl_fuzzy_parser(text:str) -> list[dict]:
    return json_repair.loads(text)

def json2dict(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

def dict2json(file_path: str) -> bool:
    return json.dump(file_path)




if __name__ == "__main__":
    pass