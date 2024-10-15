from pydantic import BaseModel


class SceneDetectionInfo(BaseModel):
    start: float
    end: float
    img_path: str
    img_timestamp: float


class SceneExtractInfo(SceneDetectionInfo):
    key: str
    has_chart: bool = False
    llm_response: list[str]


class VideoFragment(SceneExtractInfo):
    sentences: list[str]
