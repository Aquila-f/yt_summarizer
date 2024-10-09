EXTRACT_KEY_WITH_IMAGE_PROMPT_PATH = "./prompt/key_extract_with_img.txt"


def load_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def get_extract_key_with_image_prompt() -> str:
    prompt_template = load_file(EXTRACT_KEY_WITH_IMAGE_PROMPT_PATH)
    return prompt_template
