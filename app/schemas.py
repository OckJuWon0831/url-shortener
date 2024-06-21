from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime


class URL(BaseModel):
    original_url: HttpUrl
    expires_in: int

    class Config:
        from_attributes = True


class URLShort(URL):
    short_url: str
    created_at: datetime
    expires_at: datetime


class URLStats(URL):
    short_url: str
    stats: int
    created_at: datetime
    expires_at: datetime
