PROMPT_PATH = "./prompt/summary.txt"


def load_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def get_prompt(subtitle_txt: str) -> str:
    prompt_template = load_file(PROMPT_PATH)
    final_prompt = prompt_template.replace("{{article_content}}", subtitle_txt)
    return final_prompt
