from typing import List

from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pymongo import ReturnDocument

from ..db import get_db
from ..models.ticket_model import TicketCreate, TicketInDB, TicketUpdate
from ..services.ticket_agent import create_ticket

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/", response_model=TicketInDB)
async def create_ticket_route(payload: TicketCreate):
    ticket = await create_ticket(payload.user_id, payload.issue, payload.priority)
    return ticket


@router.get("/", response_model=List[TicketInDB])
async def list_tickets(status: str | None = None):
    db = get_db()
    query = {"status": status} if status else {}
    tickets = []
    async for ticket in db.tickets.find(query).sort("created_at", -1):
        ticket["_id"] = str(ticket["_id"])
        tickets.append(ticket)
    return tickets


@router.get("/{ticket_id}", response_model=TicketInDB)
async def get_ticket(ticket_id: str):
    db = get_db()
    ticket = await db.tickets.find_one({"_id": ObjectId(ticket_id)})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket["_id"] = str(ticket["_id"])
    return ticket


@router.patch("/{ticket_id}", response_model=TicketInDB)
async def update_ticket(ticket_id: str, payload: TicketUpdate):
    db = get_db()
    update_fields = {"status": payload.status}
    if payload.priority:
        update_fields["priority"] = payload.priority
    ticket = await db.tickets.find_one_and_update(
        {"_id": ObjectId(ticket_id)},
        {"$set": update_fields},
        return_document=ReturnDocument.AFTER,
    )
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket["_id"] = str(ticket["_id"])
    return ticket
