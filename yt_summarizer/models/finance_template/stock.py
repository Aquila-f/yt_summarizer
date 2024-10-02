from pydantic import BaseModel


class stock(BaseModel):
    name: str
    symbol: str
