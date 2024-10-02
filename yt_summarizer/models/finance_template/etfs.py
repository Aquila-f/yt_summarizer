from pydantic import BaseModel


class ETF(BaseModel):
    name: str
    symbol: str
