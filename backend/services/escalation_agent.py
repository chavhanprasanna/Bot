from typing import Dict

from .llm_provider import get_llm


async def summarize_issue(issue: str) -> str:
    llm = get_llm()
    prompt = (
        "Summarize the following support issue in one sentence for a human agent:\n"
        f"{issue}"
    )
    response = llm.invoke(prompt)
    return response.content.strip()


def should_escalate(message: str) -> bool:
    triggers = {"human", "manager", "angry", "complaint"}
    message_lower = message.lower()
    return any(trigger in message_lower for trigger in triggers)


def escalation_payload(user_id: str, issue: str, summary: str) -> Dict:
    return {
        "user_id": user_id,
        "issue": issue,
        "summary": summary,
        "status": "Escalated",
    }
