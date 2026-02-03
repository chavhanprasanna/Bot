from datetime import datetime
from typing import Dict

from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .config import settings
from .db import close_mongo_connection, connect_to_mongo, get_db
from .routes.admin_routes import router as admin_router
from .routes.faq_routes import router as faq_router
from .routes.ticket_routes import router as ticket_router
from .services.escalation_agent import escalation_payload, should_escalate, summarize_issue
from .services.faq_agent import score_faqs
from .services.ticket_agent import create_ticket

app = FastAPI(title="Customer Support AI Chatbot")


class ChatRequest(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    status: str
    ticket_id: str | None = None
    escalation: Dict | None = None
    confidence: float | None = None


@app.on_event("startup")
async def startup_event() -> None:
    connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    close_mongo_connection()


app.include_router(ticket_router)
app.include_router(faq_router)
app.include_router(admin_router)


@app.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    db = get_db()
    message = payload.message

    if should_escalate(message):
        summary = await summarize_issue(message)
        ticket = await create_ticket(payload.user_id, message, priority="high")
        await db.tickets.update_one(
            {"_id": ObjectId(ticket["_id"])}, {"$set": {"status": "Escalated"}}
        )
        escalation = escalation_payload(payload.user_id, message, summary)
        await db.conversations.insert_one(
            {
                "user_id": payload.user_id,
                "messages": [message, summary],
                "timestamp": datetime.utcnow(),
            }
        )
        return ChatResponse(
            response="I've escalated this to a human agent for immediate help.",
            status="Escalated",
            ticket_id=ticket["_id"],
            escalation=escalation,
            confidence=1.0,
        )

    faqs = []
    async for faq in db.faqs.find({}):
        faqs.append({"question": faq.get("question"), "answer": faq.get("answer")})

    answer, confidence = score_faqs(message, faqs)

    if not answer or confidence < settings.faq_confidence_threshold:
        ticket = await create_ticket(payload.user_id, message, priority="medium")
        await db.conversations.insert_one(
            {
                "user_id": payload.user_id,
                "messages": [message, "Ticket created"],
                "timestamp": datetime.utcnow(),
            }
        )
        return ChatResponse(
            response=(
                "Thanks! I've opened a support ticket and our team will follow up."
            ),
            status="Open",
            ticket_id=ticket["_id"],
            confidence=confidence,
        )

    await db.conversations.insert_one(
        {
            "user_id": payload.user_id,
            "messages": [message, answer],
            "timestamp": datetime.utcnow(),
        }
    )
    return ChatResponse(
        response=answer,
        status="Resolved",
        confidence=confidence,
    )


@app.get("/health")
async def health_check():
    if not settings.mongo_uri:
        raise HTTPException(status_code=500, detail="MongoDB not configured")
    return {"status": "ok"}
