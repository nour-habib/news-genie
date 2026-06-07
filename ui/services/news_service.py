import requests
import streamlit as streamlit
import os

@streamlit.cache_data(ttl=3600)
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
            "sortBy": "popularity"
        }
    )

    response.raise_for_status()
    response_json = response.json()

    print(f"Response status: {response_json.get('status')}")
    print(f"Total articles: {len(response_json.get('articles', []))}")

    return response_json
