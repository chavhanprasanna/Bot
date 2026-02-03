from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    user_id: str
    issue: str
    priority: str = "medium"


class TicketUpdate(BaseModel):
    status: str
    priority: Optional[str] = None


class TicketInDB(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    issue: str
    status: str
    priority: str
    created_at: datetime
