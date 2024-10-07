PROMPT_PATH = "./prompt/summary.txt"
EXTRACT_KEY_PROMPT_PATH = "./prompt/key_extract.txt"


def load_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def get_prompt(subtitle_txt: str) -> str:
    prompt_template = load_file(PROMPT_PATH)
    final_prompt = prompt_template.replace("{{article_content}}", subtitle_txt)
    return final_prompt


def get_extract_key_prompt(subtitle_txt: str) -> str:
    prompt_template = load_file(EXTRACT_KEY_PROMPT_PATH)
    final_prompt = prompt_template.replace("{{article_content}}", subtitle_txt)
    return final_prompt
