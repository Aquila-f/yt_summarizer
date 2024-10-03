from pydantic import BaseModel


class Forex(BaseModel):
    name: str
    symbol: str
