from typing import Optional

from pydantic import BaseModel, Field


class EconomicIndicator(BaseModel):
    name: Optional[str] = Field(
        None,
        description="The name of the economic indicator, e.g., GDP, Unemployment Rate",
    )
    impact_summary: Optional[str] = Field(
        None,
        description="Summary of the speaker's discussion on how the indicator impacts the market",
    )
    trend_analysis: Optional[str] = Field(
        None,
        description="Analysis of the trend related to this indicator, as discussed in the video",
    )
    market_response: Optional[str] = Field(
        None,
        description="The expected or predicted market response to changes in this indicator, according to the speaker",
    )
