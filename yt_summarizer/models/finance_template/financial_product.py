from typing import Optional

from pydantic import BaseModel, Field


class FinancialProduct(BaseModel):
    name: Optional[str] = Field(None, description="The name of the financial product")
    symbol: Optional[str] = Field(
        None, description="The trading symbol for the product"
    )
    market_type: Optional[str] = Field(
        None, description="The market type, e.g., stock, bond, ETF"
    )
    summary: Optional[str] = Field(
        None,
        description="A brief summary about the financial product, highlighting key points discussed in the video",
    )
    sentiment: Optional[str] = Field(
        None,
        description="The overall sentiment of the finance section (e.g., positive, negative, neutral).",
    )
