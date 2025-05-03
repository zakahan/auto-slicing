import json_repair


def jsonl_parser(text:str) -> list[dict]:
    return json_repair.loads(text)


if __name__ == "__main__":
    pass