from typing import TypedDict

class AgentState(TypedDict):
    query: str
    response: str
    session_id: str
    