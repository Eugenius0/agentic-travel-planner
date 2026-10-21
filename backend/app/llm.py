import os

from langchain_groq import ChatGroq


def create_llm() -> ChatGroq:
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")

    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not configured")

    return ChatGroq(
        model=model,
        api_key=api_key,
        temperature=0.3,
        max_retries=0,
        timeout=30,
    )
