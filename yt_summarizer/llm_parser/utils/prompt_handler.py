import base64

from langchain_core.messages import HumanMessage, SystemMessage

from yt_summarizer.llm_parser.utils.llm import get_openai_model
from yt_summarizer.llm_parser.utils.prompt import load_file
from yt_summarizer.utils.image_handler import ImageHandler

EXTRACT_KEY_WITH_IMAGE_PROMPT_PATH = "./prompt/key_extract_with_img.txt"

llm = get_openai_model("gpt-4o")
key_extract_prompt = load_file(EXTRACT_KEY_WITH_IMAGE_PROMPT_PATH)


def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/png;base64,{base64_image}"


def key_extract_with_image_prompt(image_path: str) -> str:
    base64_img = ImageHandler.resize_and_convert_image_to_base64(image_path)
    messages = [
        SystemMessage(content=key_extract_prompt),
        HumanMessage(
            content=[
                {
                    "type": "image_url",
                    "image_url": {
                        "url": base64_img,
                    },
                }
            ]
        ),
    ]
    return messages
