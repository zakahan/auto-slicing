import random
import string
from google.genai import types
from google.adk.agents import RunConfig
from google.adk.runners import Runner
from agent_kit.dto import RunResponse, create_text_response


def create_response_id():
    # 输出一个长度为16位，包括0-9;a-z;A-Z的随机字符串，作为response_id
    return "".join(random.choices(string.ascii_letters + string.digits, k=16))


async def run_by_single_turn(
    runner: Runner,
    prompt: str,
    run_config: RunConfig,
    user_id: str,
    session_id: str,
    response_id: str = "",
) -> list[RunResponse]:
    if not response_id:
        response_id = create_response_id()

    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    output_list = []
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message,
        run_config=run_config,
    ):
        if event.is_final_response():
            output_list.append(
                create_text_response(
                    author=event.author,
                    text=event.content.parts[0].text,
                    response_id=response_id,
                    session_id=session_id,
                )
            )

    return output_list


async def run_by_multi_turn(
    runner: Runner,
    querys: list[str],
    run_config: RunConfig,
    user_id: str,
    session_id: str,
) -> list[RunResponse]:
    result_list = []
    response_id = create_response_id()
    for query in querys:
        output_list = await run_by_single_turn(
            runner=runner,
            prompt=query,
            run_config=run_config,
            user_id=user_id,
            session_id=session_id,
            response_id=response_id,
        )
        result_list.extend(output_list)

    return result_list
