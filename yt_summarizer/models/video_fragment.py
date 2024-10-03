from pydantic import BaseModel


class SceneDetectionInfo(BaseModel):
    start: float
    end: float
    img_timestamp: float
