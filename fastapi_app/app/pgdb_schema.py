from typing import List, Optional

from pydantic import BaseModel

class StockBase(BaseModel):
    symbol: str
    description: Optional[str] = None
    figi: Optional[str] = None
    type: Optional[str] = None

class StockCreate(StockBase):
    pass

class Stock(StockBase):
    id: int

    class Config:
        orm_mode = True