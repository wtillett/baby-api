from typing import Optional
from pydantic import BaseModel


class BottleInput(BaseModel):
    id: Optional[int] = None
    date: Optional[str] = None
    time: Optional[str] = None
    amount: str
