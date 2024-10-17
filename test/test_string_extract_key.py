import json

import pytest

from yt_summarizer.llm_parser.string_extractor import StringExtractor

TEST_FILE = "test/data/string_extract_key_tests.json"


class TestKeyStringExtract:
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
            result = StringExtractor.get_key_topic(input_str)
            assert result == expected_output, f"Failed for input: {input_str}"

    def test_multiple_cases(self, load_test_data):
        multiple_cases = load_test_data["multiple_cases"]
        for case in multiple_cases:
            input_str = case["input"]
            expected_output = case["expect"]
            result = StringExtractor.get_key_topic(input_str)
            assert result == expected_output, f"Failed for input: {input_str}"

    def test_punctuation_cases(self, load_test_data):
        punctuation_cases = load_test_data["punctuation_cases"]
        for case in punctuation_cases:
            input_str = case["input"]
            expected_output = case["expect"]
            result = StringExtractor.get_key_topic(input_str)
            assert result == expected_output, f"Failed for input: {input_str}"
