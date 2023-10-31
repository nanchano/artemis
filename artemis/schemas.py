from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Event(BaseModel):
    id: int
    name: str
    description: str
    category: str
    location: str
    publisher: str
    start_ts: datetime
    end_ts: datetime


class CreateEvent(BaseModel):
    name: str
    description: str
    category: str
    location: str
    publisher: str
    start_ts: datetime
    end_ts: datetime


class UpdateEvent(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    publisher: Optional[str] = None
    start_ts: Optional[datetime] = None
    end_ts: Optional[datetime] = None
