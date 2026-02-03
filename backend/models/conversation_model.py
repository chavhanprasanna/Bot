from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class ConversationCreate(BaseModel):
    user_id: str
    messages: List[str]


class ConversationInDB(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    messages: List[str]
    timestamp: datetime
