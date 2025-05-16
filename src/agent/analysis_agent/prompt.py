import textwrap  

AGENT_DESCRIPTION = """
你是一个热点信息捕捉专家，你现在要做这样的一个任务：
现在有一段视频，来自于一名主播的直播录像，你将扮演一个视频切片员，提取出值得切出来的部分，并总结出切片的标题。前面的流程中，
已经将该视频进行了语音转文本处理，接下来提供给你的内容就是这段文本信息。
"""

AGENT_INSTRUCTION = """
文字内容已经提前分为多个切片，但他们仅仅是按照语音的情况切分的，太过于细粒度了，我希望你能做基于内容关联的中等细粒度的切分
将会以jsonl的格式提供给你，每个json包括三个字段，"start_time"， "stop_time"和"text"。
其中start_time和stop_time是时间标记（以秒为单位），按时间顺序二者共同标识一条切片，text是这段内容的文本。你必须审查text中哪里有值得提取的部分，并将这些部分选出来。
并且给出一个总结作为切片视频的标题。

额外命令：关于标题，我不希望是那种总结全文式的标题，我更希望是针对这个片段的标题，要有新意要有吸引力，不要就仅仅是xx在做xxx事情这样的太笼统的概括，偶尔要局部一些
这里是几个参考样例标题：
1. 做全麻在病房胡言乱语大喊大叫我是星瞳 我是明星 我6月要办演唱会【星瞳】
2. 瞳姐难绷相亲相到雏草姬 怎么有人名字叫"关注塔菲谢谢喵"啊😅【星瞳】
3. 招笑瞳姐觉得自己穿过的衣服能卖2w一件🤣【星瞳】
4. 瞳姐难绷互联网大厂员工不知道工作站电脑开机键在哪【星瞳】
"""
# 此处特别致谢恨也迷人，偷了几个标题，用来给LLM参考学习


def get_analysis_prompt(query: str, introduction:str, key:str = 'easy'):
    easy_prompt = textwrap.dedent(
    f"""
    ### 你的返回内容应该采取如下的形式
    ```json
    [
        {{
            "start_time": "来自于输入的start_time字段，表示要切分的视频的开始，而且要讲清楚前因后果",
            "stop_time": "来自于输入的stop_time字段，表示要切分的的视频的结束"而且要讲清楚前因后果,
            "title": "表示这段切片视频的标题",
        }},
        // 如果你认为这一段录播有多个值得切片的地方，请你继续提出，并且要求前后切片不能有重叠，但你不要切太多，切片的精髓是关键！而不是堆数量！
    ]
    ```\n\n""" 
    )

    two_step_prompt = textwrap.dedent(
        "暂时我还没想明白咋搞这个，其实前面clip的那个也是我瞎编的，这部分没想好"
    )

    prompt_dict = {
        'easy': easy_prompt,
        'two_step': two_step_prompt
    }   
    if key not in prompt_dict:
        raise KeyError(f"Please set a usable key. I don't know what this '{key}' you found is.")

    back_prompt = f"### 首先给你介绍一下主播的基本信息：\n{introduction}，\n### 切片内容分别如下：\n{str(query)}"
    return prompt_dict[key] + back_prompt
