from pydantic import BaseModel


class LLMResponse(BaseModel):
    content: str


class ImageKeyResponse(LLMResponse):
    key: str
    has_chart: bool = False
