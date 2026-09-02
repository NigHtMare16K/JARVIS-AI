from app.core.config import GROQ_API_KEY
from langchain_groq import ChatGroq

def get_llm():
    return ChatGroq(
        api_key = GROQ_API_KEY,
        model="llama-3.3-70b-versatile",
        temperature=0.7
    )