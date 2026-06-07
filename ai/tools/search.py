import streamlit as st
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from models import SearchResponse

def _search_news(query: str) -> SearchResponse:
    searcher = TavilySearchResults(
        max_results = MAX_RESULTS,
        api_key = os.getenv("TAVILY")
    )


