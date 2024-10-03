from pydantic import BaseModel, Field

from yt_summarizer.models.finance_template.etfs import ETF
from yt_summarizer.models.finance_template.forex import Forex
from yt_summarizer.models.finance_template.stock import Stock


class FinanceSummary(BaseModel):
    stocks: list[Stock] = Field(
        [],
        description="A list of individual stocks. If no stocks are available, leave this list empty.",
    )
    etfs: list[ETF] = Field(
        [],
        description="A list of ETFs (Exchange-Traded Funds). If no ETFs are available, leave this list empty.",
    )
    forex: list[Forex] = Field(
        [],
        description="A list of forex pairs. If no forex pairs are available, leave this list empty.",
    )
