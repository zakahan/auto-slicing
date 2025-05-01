import json_repair


def jsonl_parser(text:str) -> list[dict]:
    return json_repair.loads(text)


if __name__ == "__main__":
    t = """
    ```json
[
    {
        "start_id": "28",
        "stop_id": "94",
        "title": "露露聊《赤壁》电影，分享对三国人物的独特看法【雫るる_Official】"
    },
    {
        "start_id": "104",
        "stop_id": "115",
        "title": "露露解读《赤壁》中关羽与曹操的关系，剖析电影情节【雫るる_Official】"
    },
    {
        "start_id": "122",
        "stop_id": "128",
        "title": "露露谈粉丝送的生日礼物与孙子兵法，表达学习意愿【雫るる_Official】"
    },
    {
        "start_id": "143",
        "stop_id": "165",
        "title": "露露探讨《赤壁》中孙权与刘备的情节，发表个人见解【雫るる_Official】"
    },
    {
        "start_id": "172",
        "stop_id": "210",
        "title": "露露谈对三国人物的喜好，感慨曹操的结局【雫るる_Official】"
    },
    {
        "start_id": "224",
        "stop_id": "232",
        "title": "露露与直播间观众讨论“清澈”一词的用法【雫るる_Official】"
    },
    {
        "start_id": "233",
        "stop_id": "248",
        "title": "露露分享在日本学中文的考试情况，对比难度【雫るる_Official】"
    },
    {
        "start_id": "269",
        "stop_id": "277",
        "title": "露露提议尝试三国相关内容，分享看三国的感受【雫るる_Official】"
    },
    {
        "start_id": "285",
        "stop_id": "289",
        "title": "露露疑惑大家对卑弥呼的了解，谈及占卜相关【雫るる_Official】"
    }
]
```
    """

    x = jsonl_parser(t)
    print(x)