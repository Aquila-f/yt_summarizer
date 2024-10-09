import base64
import os


def load_prompt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def is_exist(file_path: str) -> bool:
    return os.path.exists(file_path)
