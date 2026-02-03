import os

from langchain_groq import ChatGroq


def get_llm() -> ChatGroq:
    return ChatGroq(
        model="llama3-8b-8192",
        api_key=os.getenv("GROQ_API_KEY"),
    )
