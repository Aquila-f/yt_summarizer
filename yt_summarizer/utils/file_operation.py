import json
import os

from pydantic import BaseModel


def load_prompt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def is_exist(file_path: str) -> bool:
    return os.path.exists(file_path)


def save_list(data: list[BaseModel], file_path: str):
    with open(file_path, "w") as file:
        json.dump(
            [item.model_dump() for item in data], file, indent=4, ensure_ascii=False
        )
