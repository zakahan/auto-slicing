import os
from google.adk.models.lite_llm import LiteLlm

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")


def create_inference_model(model_type="normal"):
    if model_type == 'normal':
        model_name = os.getenv("OPENAI_MODEL")
    else: # 'thinking
        model_name = os.getenv("OPENAI_MODEL_THINKING")
    model_name = model_name
    return LiteLlm(
        model=f"openai/{model_name}",
        api_key=OPENAI_API_KEY,
        api_base=OPENAI_API_BASE
    )