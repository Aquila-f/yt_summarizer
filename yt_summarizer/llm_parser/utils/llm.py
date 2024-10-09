import os

from langchain_openai import ChatOpenAI


def get_openai_model(
    model_name: str = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
) -> ChatOpenAI:
    model_name = model_name
    return ChatOpenAI(model=model_name, temperature=0)
