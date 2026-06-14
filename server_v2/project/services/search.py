import os
from tavily import TavilyClient
from config import Config

def search_real_estate(query: str, location: str = None) -> str:
    """
    Search real estate listings or market info using Tavily.
    """
    api_key = Config.TAVILY_API_KEY
    if not api_key:
        # Fallback if config has no key
        return "⚠️ Web search is currently disabled because TAVILY_API_KEY is not configured in .env."

    api_key = api_key.strip('"\'')
    if api_key == "your_tavily_api_key_here":
        return "⚠️ Web search is currently disabled because TAVILY_API_KEY is still set to placeholder."

    try:
        client = TavilyClient(api_key=api_key)
        
        # Build search query
        search_query = query
        if location and location.lower() not in query.lower():
            search_query = f"{query} in {location}"

        # Perform search
        response = client.search(
            query=search_query,
            search_depth="advanced",
            topic="general",
            max_results=3
        )

        results = response.get("results", [])
        if not results:
            return "No listings or information found on the web."

        formatted_results = []
        for idx, res in enumerate(results, 1):
            title = res.get("title", "No Title")
            url = res.get("url", "")
            content = res.get("content", "")
            formatted_results.append(
                f"{idx}. **{title}**\n   Url: {url}\n   Summary: {content}\n"
            )

        return "\n".join(formatted_results)

    except Exception as e:
        return f"Error executing search: {str(e)}"
