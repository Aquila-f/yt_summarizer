from pydantic import BaseModel


class Trend(BaseModel):
    name: str
    symbol: str
