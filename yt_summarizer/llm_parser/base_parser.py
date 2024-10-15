from abc import ABC, abstractmethod

from yt_summarizer.models.llm_response import LLMResponse


class BaseParser(ABC):
    @abstractmethod
    def parse(self, content: str) -> LLMResponse:
        raise NotImplementedError
