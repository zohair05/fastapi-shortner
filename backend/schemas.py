from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import List, Optional

class URLCreate(BaseModel):
    long_url: HttpUrl

class URLResponse(BaseModel):
    short_code: str
    long_url: str
    created_at: datetime

    class Config:
        from_attributes = True

class ClickData(BaseModel):
    timestamp: datetime
    ip_address: Optional[str]
    user_agent: Optional[str]

class AnalyticsResponse(BaseModel):
    long_url: str
    total_clicks: int
    clicks: List[ClickData]