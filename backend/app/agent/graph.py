from langgraph.graph import StateGraph, START, END

from app.agent.state import AgentState
from app.services.llm_service import generate_response


def llm_node(state: AgentState):
    result = generate_response(
        state["query"],
        state["session_id"]
    )

    return {
        "response": result["answer"]
    }


builder = StateGraph(AgentState)

builder.add_node("llm", llm_node)

builder.add_edge(START, "llm")
builder.add_edge("llm", END)

graph = builder.compile()


result = graph.invoke({
    "query": "What is a LLM",
    "session_id": "user-1",
    "response": ""
})

print(result["response"])