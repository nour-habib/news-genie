import requests
import streamlit as streamlit
import os
from tavily import TavilyClient
from functools import lru_cache

@lru_cache(maxsize=20)
def get_articles(category: str):
    api_key = os.getenv("NEWS_API_KEY")

    if not api_key:
        raise ValueError("NEWS_API_KEY not set in environment variables")

    response = requests.get(
        "https://newsapi.org/v2/top-headlines",
        params={
            "category": category,
            "apiKey": api_key,
            "country": "us",
            "sortBy": "popularity",
        }
    )

    response.raise_for_status()
    response_json = response.json()

    print(f"Response status: {response_json.get('status')}")
    print(f"Total articles: {len(response_json.get('articles', []))}")

    # Verify articles
    articles = response_json.get('articles', [])
    articles = verify_articles(articles)
    response_json['articles'] = articles

    return response_json


def verify_articles(articles: list) -> list:
    """
    Verify each article and add veracity_score (1-5).
    """
    from ai.agents.verification_agent import run as verify

    for article in articles:
        try:
            # Create Article object for verification
            from ai.models.article import Article
            article_obj = Article(
                title=article.get('title', ''),
                description=article.get('description', ''),
                source=article.get('source', {}).get('name', 'Unknown'),
                url=article.get('url', '')
            )
            # Get veracity score
            article['veracity_score'] = verify(article_obj)
        except Exception as e:
            print(f"Error verifying article: {e}")
            article['veracity_score'] = 3  # Default to neutral

    return articles


def web_search(query: str, num_results: int = 3) -> str:
    """
    Search the web using Tavily and return formatted results.
    """
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "Error: TAVILY_API_KEY not set"

        client = TavilyClient(api_key=api_key)
        response = client.search(query, max_results=num_results)

        # Format results
        results = "Web search results:\n"
        for i, result in enumerate(response.get("results", []), 1):
            results += f"\n{i}. {result.get('title', 'No title')}\n"
            results += f"   {result.get('content', 'No content')[:200]}...\n"
            results += f"   Source: {result.get('url', 'No URL')}\n"

        return results
    except Exception as e:
        return f"Error searching the web: {str(e)}"


def ask_ai(query: str, chat_history: list = None) -> str:
    import traceback
    print(f"DEBUG: ask_ai called with query: {query}")

    try:
        print("DEBUG: Importing router...")
        from ai.agents.router import run_query
        print("DEBUG: Router imported successfully")

        # Format chat history as context if provided
        context = ""
        if chat_history:
            context = "Previous conversation:\n"
            for msg in chat_history[-4:]:  # Last 4 messages for context
                role = "User" if msg["role"] == "user" else "Assistant"
                context += f"{role}: {msg['content']}\n"
            context += "\n"

        full_query = context + f"Current question: {query}"

        print("DEBUG: Calling run_query...")
        response = run_query(full_query)
        print(f"DEBUG: Got response: {response}")
        return response
    except Exception as e:
        print(f"DEBUG: Exception caught: {e}")
        traceback.print_exc()
        return f"Error processing query: {str(e)}"



