from pydantic import BaseModel


class YTInfo(BaseModel):
    url: str
    title: str
    length: int
    author: str
    channel_url: str
    thumbnail_url: str
    views: int
