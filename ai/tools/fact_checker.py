import streamlit as st
from models import Article
from langchain.tools import tool


#Config

RED_FLAGS = [
    "BREAKING",
    "SHOCKING",
    "DOCTORS HATE THIS",
    "CLICK HERE",
    "YOU WON'T BELIEVE",
    "FAKE",
    "HOAX"
]


#Methods
def quick_check(article: Article) -> bool:
    """
    Quick local check for obvious red flags.
    Returns True if article looks suspicious, False if it looks legitimate.
    """
    title = article.title.upper()
    description = (article.description or "").upper()

    for flag in RED_FLAGS:
        if flag in title or flag in description:
            return True

    return False


@st.cache_data(ttl=86400)
def _factcheck_article(article: Article) -> bool:
    """
    Main fact-checker function.
    Returns True if article appears suspicious, False if legitimate.
    """
    return quick_check(article)


#LangChain tool wrapper
@tool
def  factcheck_tool(article: Article) -> bool:
    return _factcheck_article(article)