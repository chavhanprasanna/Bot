from typing import Dict, List, Tuple


def score_faqs(query: str, faqs: List[Dict[str, str]]) -> Tuple[str | None, float]:
    query_lower = query.lower()
    best_answer = None
    best_score = 0.0
    for faq in faqs:
        question = faq.get("question", "").lower()
        if not question:
            continue
        match_score = 0.0
        if query_lower in question or question in query_lower:
            match_score = 0.9
        else:
            shared = set(query_lower.split()) & set(question.split())
            if shared:
                match_score = min(0.6 + (0.05 * len(shared)), 0.85)
        if match_score > best_score:
            best_score = match_score
            best_answer = faq.get("answer")
    return best_answer, best_score
