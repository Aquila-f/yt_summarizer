from typing import Optional

from pydantic import BaseModel


class SubtitleUrl(BaseModel):
    lang: str
    ext: str
    url: str
    name: str


class YTInfo(BaseModel):
    url: str
    title: str
    length: int
    author: str
    channel_url: str
    thumbnail_url: str
    views: int
    subtitle: Optional[SubtitleUrl]


class Segment(BaseModel):
    start: float
    end: float
    text: str
