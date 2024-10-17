import re
import string


class StringExtractor:
    @staticmethod
    def get_key_topic(result: str) -> str:
        matches = re.findall(r"\[\[.*?\]\]", result)
        if matches:
            last_match = matches[-1]
            punctuation = string.punctuation.replace("&", "")
            translator = str.maketrans("", "", punctuation)
            return last_match.translate(translator).upper().replace(" ", "")
        return ""

    @staticmethod
    def has_chart(result: str) -> bool:
        matches = re.findall(r"\{\{.*?\}\}", result)
        if matches:
            last_match = matches[-1]
            return last_match.upper().replace(" ", "") == "{{YES}}"
        return False
