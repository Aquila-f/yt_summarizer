import json

import pytest

from yt_summarizer.llm_parser.image_key_parser import ImageKeyParser

TEST_FILE = "test/data/key_extract_post_process_tests.json"


class TestKeyExtractLLMParser:
    @pytest.fixture(scope="class")
    def load_test_data(self):
        with open(TEST_FILE, "r") as file:
            data = json.load(file)
        return data

    def test_base_cases(self, load_test_data):
        base_cases = load_test_data["base_cases"]
        for case in base_cases:
            input_str = case["input"]
            expected_output = case["expect"]
            result = ImageKeyParser.post_process(input_str)
            assert result == expected_output, f"Failed for input: {input_str}"

    def test_multiple_cases(self, load_test_data):
        multiple_cases = load_test_data["multiple_cases"]
        for case in multiple_cases:
            input_str = case["input"]
            expected_output = case["expect"]
            result = ImageKeyParser.post_process(input_str)
            assert result == expected_output, f"Failed for input: {input_str}"

    def test_punctuation_cases(self, load_test_data):
        punctuation_cases = load_test_data["punctuation_cases"]
        for case in punctuation_cases:
            input_str = case["input"]
            expected_output = case["expect"]
            result = ImageKeyParser.post_process(input_str)
            assert result == expected_output, f"Failed for input: {input_str}"
