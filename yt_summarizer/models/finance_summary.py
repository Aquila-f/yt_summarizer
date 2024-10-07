from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field

from yt_summarizer.models.finance_template.economic_indicator import EconomicIndicator
from yt_summarizer.models.finance_template.financial_product import FinancialProduct
from yt_summarizer.models.finance_template.market_trend import MarketTrend


class FinanceSummary(BaseModel):
    financial_product: Optional[FinancialProduct] = Field(
        None, description="Summary of key financial products discussed"
    )
    economic_indicators: Optional[EconomicIndicator] = Field(
        None, description="Summary of important economic indicators mentioned"
    )
    market_trends: Optional[MarketTrend] = Field(
        None, description="Overview of market trends highlighted"
    )
    overall_summary: str = Field(
        str, description="Comprehensive summary of all key points"
    )
