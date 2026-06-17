import requests
import streamlit as streamlit
import os
from datetime import datetime


_cache = {}


def fetch_articles(category: str):
    """Fetch articles from NewsAPI and verify them."""
    try:
        api_key = os.getenv("NEWS_API_KEY")

        if not api_key:
            return {
                "status": "error",
                "articles": [],
                "error_message": "❌ NewsAPI key not entered."
            }

        response = requests.get(
            "https://newsapi.org/v2/top-headlines",
            params={
                "category": category,
                "apiKey": api_key,
                "country": "us",
                "sortBy": "popularity",
            },
            timeout=5
        )

        if response.status_code == 401:
            return {
                "status": "error",
                "articles": [],
                "error_message": "NewsService Error: Invalid NewsAPI key"
            }
        elif response.status_code == 429:
            return {
                "status": "error",
                "articles": [],
                "error_message": "NewsService Error: Rate limit exceeded"
            }
        elif response.status_code != 200:
            return {
                "status": "error",
                "articles": [],
                "error_message": f"NewsService Erro : error ({response.status_code})"
            }

        response_json = response.json()

        if response_json.get("status") == "error":
            return {
                "status": "error",
                "articles": [],
                "error_message": f"❌ NewsAPI error: {response_json.get('message', 'Unknown error')}"
            }

        print(f"Response status: {response_json.get('status')}")
        print(f"Total articles: {len(response_json.get('articles', []))}")

        # Verify articles
        from ai.agents.router import verify_articles
        articles = response_json.get('articles', [])
        articles = verify_articles(articles)
        response_json['articles'] = articles

        return response_json

    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "articles": [],
            "error_message": "❌ NewsAPI request timed out. Please try again."
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "articles": [],
            "error_message": "❌ Connection error. Please check your internet connection."
        }
    except Exception as e:
        return {
            "status": "error",
            "articles": [],
            "error_message": f"❌ Unexpected error: {str(e)}"
        }


def get_articles(category: str):
    #Get articles with custom cache logic: refresh at 7am or when empty
    now = datetime.now()
    time = now.time()

    should_refresh = (category not in _cache) or (time.hour == 7)

    if should_refresh:
        data = fetch_articles(category)
        _cache[category] = data
        return data

    return _cache[category]


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
