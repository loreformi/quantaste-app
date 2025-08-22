
from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class TickerBase(BaseModel):
    symbol: str
    company_name: Optional[str] = None

class TickerCreate(TickerBase):
    pass

class Ticker(TickerBase):
    id: int

    class Config:
        from_attributes = True

class DailyScoreBase(BaseModel):
    date: date
    final_score: float
    smoothed_score: float
    label: str

class DailyScore(DailyScoreBase):
    id: int
    ticker_id: int

    class Config:
        from_attributes = True

class TickerScoreResponse(BaseModel):
    id: int
    symbol: str
    company_name: Optional[str] = None
    latest_score: Optional[DailyScoreBase] = None

class TickerDetailResponse(TickerBase):
    id: int
    scores: List[DailyScoreBase] = []
