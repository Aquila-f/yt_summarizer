import re
import string

from langchain_core.messages import HumanMessage, SystemMessage

from yt_summarizer.llm_parser.base_parser import BaseParser
from yt_summarizer.llm_parser.string_extractor import StringExtractor
from yt_summarizer.llm_parser.utils.llm import get_openai_model
from yt_summarizer.models.llm_response import ImageKeyResponse
from yt_summarizer.utils.file_operation import load_prompt
from yt_summarizer.utils.image_handler import ImageHandler

""" content of EXTRACT_KEY_WITH_IMAGE_PROMPT
You are a helpful assistant! Please follow the instructions below precisely to avoid any unintended outcomes. The user will provide you with a single image, and you are to process it by following the steps outlined below and answering the questions accordingly:

Step 1: Describe the image provided by the user.
Step 2: Identify the main subject of the image.
Step 3: Determine if the main subject of the image relates to a tradable financial product.
Step 4: If the subject is not a tradable financial product, return the value [[others]]. If it is, proceed to Step 5.
Step 5: Do you recognize the name of this financial product? What is its trading symbol in the stock market?
Step 6: If you know the trading symbol, return it using the following format: [[symbol]]
"""


class ImageKeyParser(BaseParser):
    EXTRACT_KEY_WITH_IMAGE_PROMPT_PATH = "./prompt/key_extract_with_img.txt"
    system_prompt = load_prompt(EXTRACT_KEY_WITH_IMAGE_PROMPT_PATH)

    def __init__(self):
        self.llm = get_openai_model("gpt-4o")

    @classmethod
    def get_complete_prompt(cls, image_path: str) -> str:
        base64_img = ImageHandler.resize_and_convert_image_to_base64(image_path)
        messages = [
            SystemMessage(content=cls.system_prompt),
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

    def parse(self, image_path: str) -> ImageKeyResponse:
        prompt = self.get_complete_prompt(image_path)
        result = self.llm.invoke(prompt)
        return ImageKeyResponse(
            key=StringExtractor.get_key_topic(result.content),
            has_chart=StringExtractor.has_chart(result.content),
            content=result.content,
        )
