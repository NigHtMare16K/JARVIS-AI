from app.core.config import GROQ_API_KEY, settings

from langchain_groq import ChatGroq

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

from langchain_core.runnables.history import RunnableWithMessageHistory


store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()

    history = store[session_id]
    # Trim in-memory history to limit API usage
    max_msgs = settings.MAX_HISTORY_MESSAGES * 2
    if len(history.messages) > max_msgs:
        history.messages = history.messages[-max_msgs:]

    return history


def get_llm():
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model=settings.GROQ_MODEL,
        temperature=settings.LLM_TEMPERATURE,
    )


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are Jarvis, an intelligent AI voice assistant.
        Answer the user's query clearly and helpfully. Keep responses concise."""
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{query}"),
])

llm = get_llm()
chain = prompt | llm

conversation_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="query",
    history_messages_key="history",
)


def generate_response(query: str, session_id: str):
    """Plain LLM response (used as fallback). Prefer run_agent for tool access."""
    response = conversation_chain.invoke(
        {"query": query},
        config={"configurable": {"session_id": session_id}},
    )
    return {"answer": response.content}
