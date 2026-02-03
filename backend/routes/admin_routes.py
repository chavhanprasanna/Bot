from typing import Dict, List

from fastapi import APIRouter

from ..db import get_db
from ..models.ticket_model import TicketInDB

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/tickets", response_model=List[TicketInDB])
async def admin_list_tickets(status: str | None = None):
    db = get_db()
    query = {"status": status} if status else {}
    tickets = []
    async for ticket in db.tickets.find(query).sort("created_at", -1):
        ticket["_id"] = str(ticket["_id"])
        tickets.append(ticket)
    return tickets


@router.get("/stats", response_model=Dict[str, int])
async def admin_stats():
    db = get_db()
    statuses = ["Open", "Pending", "Resolved", "Escalated"]
    stats = {}
    for status in statuses:
        stats[status] = await db.tickets.count_documents({"status": status})
    return stats
