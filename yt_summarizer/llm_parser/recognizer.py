from yt_summarizer.llm_parser.utils.llm import get_openai_model
from yt_summarizer.llm_parser.utils.prompt_handler import key_extract_with_image_prompt


def key_extract_with_image(image_path: str) -> str:
    prompt = key_extract_with_image_prompt(image_path)
    llm = get_openai_model()
    result = llm.invoke(prompt)
    print(result)
    return result
