from typing import Optional

from pydantic import BaseModel, Field


class MarketTrend(BaseModel):
    trend_description: Optional[str] = Field(
        None, description="Description of the market trend identified in the video"
    )
    affected_sectors: list[str] = Field(
        default_factory=list,
        description="Sectors that are primarily affected by this trend",
    )
    future_outlook: Optional[str] = Field(
        None,
        description="Speaker's prediction or outlook on the future direction of the market related to this trend",
    )
    impact_analysis: Optional[str] = Field(
        None,
        description="Analysis of the potential impact of this trend on the market and economy",
    )
    major_news_events: Optional[str] = Field(
        None,
        description="Description of major news events that have an impact on the market trend",
    )
