from app.core.config import GROQ_API_KEY
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate


def get_llm():
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model="openai/gpt-oss-120b",
        temperature=0.7
    )


prompt = PromptTemplate(
    template="""
    You are Jarvis, an intelligent AI voice assistant.
    Answer the user's query clearly and helpfully.

    User Query:
    {query}
    """,
    input_variables=["query"],
)

llm = get_llm()

chain = prompt | llm


def generate_response(query: str):
    response = chain.invoke({"query": query})

    return {
        "answer": response.content
    }

print(generate_response("What is Machine Learning"))