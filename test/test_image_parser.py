import json

import pytest
from langchain_community.callbacks import get_openai_callback

from yt_summarizer.llm_parser.image_key_parser import ImageKeyParser

TEST_FILE = "./test/data/extract_key_tests.json"


class TestKeyExtractLLMParser:
    @pytest.fixture(scope="class")
    def load_test_data(self):
        with open(TEST_FILE, "r") as file:
            data = json.load(file)
        return data

    def test_finance_product_cases(self, load_test_data):
        finance_cases = load_test_data["finance_product_cases"]
        try:
            with get_openai_callback() as cb:
                for case in finance_cases:
                    input_img_path = case["input"]
                    expected_output = case["expect"]
                    response = ImageKeyParser().parse(input_img_path)
                    assert (
                        response.key == expected_output
                    ), f"Failed for input: {input_img_path}"
        finally:
            print(f"token: {cb.total_tokens}, cost: {cb.total_cost}")

    def test_other_cases(self, load_test_data):
        other_cases = load_test_data["other_cases"]
        try:
            with get_openai_callback() as cb:
                for case in other_cases:
                    input_img_path = case["input"]
                    expected_output = case["expect"]
                    response = ImageKeyParser().parse(input_img_path)
                    assert (
                        response.key == expected_output
                    ), f"Failed for input: {input_img_path}"
        finally:
            print(f"token: {cb.total_tokens}, cost: {cb.total_cost}")
