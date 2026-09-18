from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, SystemMessage

from app.agent.state import AgentState
from app.core.config import settings
from app.services.llm_service import llm, get_session_history
from app.tools.system import open_application, search_youtube, play_youtube
from app.tools.songs import play_spotify
from app.tools.files import open_file_or_folder
from app.tools.web_search import web_search_results
from app.tools.rag import query_active_pdf

tools = [
    open_application,
    search_youtube,
    play_youtube,
    play_spotify,
    open_file_or_folder,
    web_search_results,
    query_active_pdf,
]
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = SystemMessage(content=(
    "You are Jarvis, an intelligent AI voice assistant. "
    "Answer clearly and concisely — responses will be spoken aloud.\n\n"
    "Tool selection guide:\n"
    "- Opening apps (Notepad, Chrome, etc.) → open_application\n"
    "- YouTube search/play → search_youtube or play_youtube\n"
    "- Spotify playback → play_spotify\n"
    "- Opening folders/files (Downloads, Desktop, a PDF file) → open_file_or_folder\n"
    "- Current events, weather, recent news, general web facts → web_search_results\n"
    "- Questions about the PDF open on screen ('this PDF', 'this document', "
    "'summarize this', 'explain page N', content from active PDF) → query_active_pdf\n"
    "- General conversation, explanations, coding help (no action needed) → answer directly\n\n"
    "When using query_active_pdf results, cite page numbers naturally "
    "(e.g. 'According to page 3...'). Keep voice answers brief."
))


def _trim_history(messages):
    """Limit conversation history sent to the LLM."""
    max_msgs = settings.MAX_HISTORY_MESSAGES
    if len(messages) > max_msgs:
        return messages[-max_msgs:]
    return messages


def llm_node(state: AgentState):
    trimmed = _trim_history(state["messages"])
    response = llm_with_tools.invoke([SYSTEM_PROMPT] + trimmed)
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

    try:
        result = graph.invoke({
            "messages": history.messages + [HumanMessage(content=query)],
            "session_id": session_id,
        })

        answer = result["messages"][-1].content
        if not answer:
            answer = "I'm sorry, I couldn't generate a response."

        history.add_user_message(query)
        history.add_ai_message(answer)
        return answer

    except Exception as exc:
        import logging
        logging.getLogger(__name__).exception("Agent error")
        return f"I encountered an error: {exc}"
