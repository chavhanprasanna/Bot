from datetime import datetime
from typing import Dict

from bson import ObjectId
from pymongo import ReturnDocument

from ..db import get_db


async def create_ticket(user_id: str, issue: str, priority: str = "medium") -> Dict:
    db = get_db()
    ticket = {
        "user_id": user_id,
        "issue": issue,
        "status": "Open",
        "priority": priority,
        "created_at": datetime.utcnow(),
    }
    result = await db.tickets.insert_one(ticket)
    ticket["_id"] = str(result.inserted_id)
    return ticket


async def update_ticket_status(ticket_id: str, status: str) -> Dict | None:
    db = get_db()
    update = {"$set": {"status": status}}
    result = await db.tickets.find_one_and_update(
        {"_id": ObjectId(ticket_id)},
        update,
        return_document=ReturnDocument.AFTER,
    )
    if result:
        result["_id"] = str(result["_id"])
    return result
