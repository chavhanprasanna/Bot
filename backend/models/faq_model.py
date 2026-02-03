from pydantic import BaseModel, Field


class FAQCreate(BaseModel):
    question: str
    answer: str


class FAQInDB(BaseModel):
    id: str = Field(alias="_id")
    question: str
    answer: str
