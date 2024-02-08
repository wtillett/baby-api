from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BottleInput(BaseModel):
    id: Optional[int] = None
    date: Optional[str] = None
    time: Optional[str] = None
    amount: str


class SleepInput(BaseModel):
    id: Optional[int] = None
    start: Optional[datetime] = None
    end: Optional[datetime] = None
