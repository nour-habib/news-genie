import streamlit as streamlit
import os
from dotenv import load_dotenv
from services.news_service import get_articles

load_dotenv()

streamlit.set_page_config(layout="wide")
streamlit.title("News App")
streamlit.write("The only the news you'll need")

# Map page names to API categories
PAGE_TO_CATEGORY = {
    "🌍 World News": "general",
    "💻 Technology": "technology",
    "💰 Finance": "business",
    "🏆 Sports": "sports",
    "   Politics": "general",
    "   Science": "science"
}

with streamlit.sidebar:
    streamlit.title("Menu")

    pages = list(PAGE_TO_CATEGORY.keys())
    if "page" not in streamlit.session_state:
        streamlit.session_state.page = pages[0]

    for page in pages:
        if streamlit.session_state.page == page:
            streamlit.markdown(f"**{page}**")  # bold = selected
        else:
            if streamlit.button(page, use_container_width=True, key=page):
                streamlit.session_state.page = page
                streamlit.rerun()

    streamlit.divider()
    streamlit.button("Logout")


col1, col2 = streamlit.columns([5, 1])
with col1:
    streamlit.text_input("Search", placeholder="Ask anything", label_visibility="collapsed")
with col2:
    streamlit.button("Ask")

streamlit.divider()

# Fetch and display articles for selected page
category = PAGE_TO_CATEGORY[streamlit.session_state.page]
try:
    data = get_articles(category)
    articles = data.get("articles", [])

    if articles:
        streamlit.subheader(f"Top Articles - {streamlit.session_state.page}")
        for article in articles:
            col1, col2 = streamlit.columns([3, 1])
            with col1:
                streamlit.markdown(f"**{article['title']}**")
                streamlit.caption(article.get("description", ""))
                streamlit.caption(f"Source: {article['source']['name']}")
            with col2:
                if article.get("urlToImage"):
                    streamlit.image(article["urlToImage"], width=150)
            streamlit.divider()
    else:
        streamlit.info("No articles found for this category.")
except Exception as e:
    streamlit.error(f"Error fetching articles: {str(e)}")

