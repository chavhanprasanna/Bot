from typing import List

from fastapi import APIRouter

from ..db import get_db
from ..models.faq_model import FAQCreate, FAQInDB

router = APIRouter(prefix="/faqs", tags=["faqs"])


@router.post("/", response_model=FAQInDB)
async def create_faq(payload: FAQCreate):
    db = get_db()
    faq = payload.dict()
    result = await db.faqs.insert_one(faq)
    faq["_id"] = str(result.inserted_id)
    return faq


@router.get("/", response_model=List[FAQInDB])
async def list_faqs():
    db = get_db()
    faqs = []
    async for faq in db.faqs.find({}):
        faq["_id"] = str(faq["_id"])
        faqs.append(faq)
    return faqs
