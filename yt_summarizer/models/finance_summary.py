from pydantic import BaseModel, Field

from yt_summarizer.models.finance_template.etfs import ETF
from yt_summarizer.models.finance_template.stock import stock


class FinanceSummary(BaseModel):
    stocks: list[stock] = Field(
        [],
        description="A list of individual stocks. If no stocks are available, leave this list empty.",
    )
    etfs: list[ETF] = Field(
        [],
        description="A list of ETFs (Exchange-Traded Funds). If no ETFs are available, leave this list empty.",
    )
