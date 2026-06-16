from langchain.tools import tool
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()


@tool
def web_search(query: str) -> str:
    """Search the web using Tavily for current information about any topic."""
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "Error: TAVILY_API_KEY not configured"

        client = TavilyClient(api_key=api_key)
        response = client.search(query, max_results=3)

        # Format results
        results = []
        for i, result in enumerate(response.get("results", []), 1):
            results.append(
                f"{i}. **{result.get('title', 'No title')}**\n"
                f"   {result.get('content', 'No content')[:300]}\n"
                f"   Source: {result.get('url', 'No URL')}"
            )

        if not results:
            return "No search results found."

        return "\n\n".join(results)

    except Exception as e:
        return f"Error performing web search: {str(e)}"
