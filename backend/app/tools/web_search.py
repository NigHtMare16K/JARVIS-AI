from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

search = TavilySearch(max_results=3)


@tool
def web_search_results(query: str) -> str:
    """Search the web for current information and return relevant results."""
    print(f"🔍 web_search_results called with: {query}")
    results = search.invoke({"query": query})
    return results