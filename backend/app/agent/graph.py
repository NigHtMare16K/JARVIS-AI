from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, SystemMessage

from app.agent.state import AgentState
from app.services.llm_service import llm, get_session_history
from app.tools.system import open_application,search_youtube,play_youtube
from app.tools.songs import play_spotify
from app.tools.files import open_file_or_folder
from app.tools.web_search import web_search_results

tools = [open_application,search_youtube,play_youtube,play_spotify,open_file_or_folder,web_search_results]
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = SystemMessage(content=(
    "You are Jarvis, an intelligent AI voice assistant. "
    "Answer the user's query clearly and helpfully. "
    "Use tools when the user asks you to perform an action like opening an app."
))


def llm_node(state: AgentState):
    response = llm_with_tools.invoke([SYSTEM_PROMPT] + state["messages"])
    return {"messages": [response]}


builder = StateGraph(AgentState)
builder.add_node("llm", llm_node)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "llm")
builder.add_conditional_edges("llm", tools_condition)
builder.add_edge("tools", "llm")

graph = builder.compile()


def run_agent(query: str, session_id: str) -> str:
    history = get_session_history(session_id)

    result = graph.invoke({
        "messages": history.messages + [HumanMessage(content=query)],
        "session_id": session_id
    })

    answer = result["messages"][-1].content

    history.add_user_message(query)
    history.add_ai_message(answer)

    return answer


if __name__ == "__main__":
    print(run_agent("What is google collabin 20 words", "user-1"))