from app.core.config import GROQ_API_KEY

from langchain_groq import ChatGroq

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

from langchain_core.runnables.history import RunnableWithMessageHistory


store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:

    if session_id not in store:
        store[session_id] = ChatMessageHistory()

    return store[session_id]


def get_llm():

    return ChatGroq(
        api_key=GROQ_API_KEY,
        model="openai/gpt-oss-120b",
        temperature=0.7
    )


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are Jarvis, an intelligent AI voice assistant.
        Answer the user's query clearly and helpfully."""
    ),

    MessagesPlaceholder(variable_name="history"),

    ("human", "{query}")
])


llm = get_llm()

chain = prompt | llm


conversation_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="query",
    history_messages_key="history"
)


def generate_response(query: str, session_id: str):

    response = conversation_chain.invoke(
        {"query": query},
        config={
            "configurable": {
                "session_id": session_id
            }
        }
    )

    return {
        "answer": response.content
    }
# print(generate_response("What is Machine Learning"))

# try:
#     while True:
#         query = input("Chat : ")
#         response = generate_response(query,"1")
#         print("Answer : ", response)
# except KeyboardInterrupt:
#     print("Chat bot implemented successfully")

