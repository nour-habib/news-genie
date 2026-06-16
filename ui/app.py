import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as streamlit
from dotenv import load_dotenv
from services.news_service import get_articles, ask_ai

load_dotenv()

streamlit.set_page_config(layout="wide")
streamlit.title("NewsGenie")
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

if "show_chat" not in streamlit.session_state:
    streamlit.session_state.show_chat = False

#Top bar, query bar

col1, col2, col3 = streamlit.columns([4, 1, 1])
with col1:
    query = streamlit.text_input("Search", placeholder="Ask anything", label_visibility="collapsed")
    if(query):
        response = ask_ai(query)
        streamlit.markdown(f"**Assistant:** {response}")
with col2:
    streamlit.button("Ask")
with col3:
    if streamlit.button("💬", use_container_width=True):
        streamlit.session_state.show_chat = not streamlit.session_state.show_chat

streamlit.divider()

#Sidebar

with streamlit.sidebar:
    streamlit.title("Menu")

    pages = list(PAGE_TO_CATEGORY.keys())
    if "page" not in streamlit.session_state:
        streamlit.session_state.page = pages[0]

    for page in pages:
        if streamlit.button(page, use_container_width=True):
            streamlit.session_state.page = page

# Display articles

category = PAGE_TO_CATEGORY[streamlit.session_state.page]

if streamlit.session_state.show_chat:
    col_articles, col_chat = streamlit.columns([2, 1])

    with col_articles:
        data = get_articles(category)
        articles = data.get("articles", [])

        for i in range(0, len(articles), 3):
            cols = streamlit.columns(3)

            for j, col in enumerate(cols):
                if i + j < len(articles):
                    article = articles[i + j]
                    with col:
                        with streamlit.container(border=True):
                            streamlit.write(f"**{article['title']}**")
                            score = article.get('veracity_score', 3)
                            streamlit.caption(f"Veracity: {score}/5 {'⭐' * score}")
                            if article.get('urlToImage'):
                                streamlit.image(article['urlToImage'], use_container_width=True)
                            else:
                                streamlit.write("📷 No image available")

                            article_key = f"article_{i}_{j}"
                            if streamlit.button("📖 Read More", key=f"btn_{article_key}", use_container_width=True):
                                streamlit.session_state[article_key] = not streamlit.session_state.get(article_key, False)

                            if streamlit.session_state.get(article_key):
                                with streamlit.expander("Full Article", expanded=True):
                                    streamlit.write(f"### {article['title']}")
                                    streamlit.write(article.get('description', 'No description available'))
                                    streamlit.write(f"**Source:** {article['source']['name']}")
                                    streamlit.write(f"[Open in Browser]({article['url']})")

    with col_chat:
        streamlit.subheader("💬 Chat")

        # Initialize chat history
        if "chat_history" not in streamlit.session_state:
            streamlit.session_state.chat_history = []

        # Display chat history
        for message in streamlit.session_state.chat_history:
            with streamlit.chat_message(message["role"]):
                streamlit.markdown(message["content"])

        # Chat input
        user_input = streamlit.chat_input("Ask something...")
        if user_input:
            # Add user message to history
            streamlit.session_state.chat_history.append({"role": "user", "content": user_input})

            # Get response from AI with chat context
            response = ask_ai(user_input, streamlit.session_state.chat_history[:-1])

            # Add assistant response to history
            streamlit.session_state.chat_history.append({"role": "assistant", "content": response})

            # Display the new message
            with streamlit.chat_message("user"):
                streamlit.markdown(user_input)
            with streamlit.chat_message("assistant"):
                streamlit.markdown(response)
else:
    data = get_articles(category)
    articles = data.get("articles", [])

    for i in range(0, len(articles), 3):
        cols = streamlit.columns(3)

        for j, col in enumerate(cols):
            if i + j < len(articles):
                article = articles[i + j]
                with col:
                    with streamlit.container(border=True):
                        streamlit.write(f"**{article['title']}**")
                        score = article.get('veracity_score', 3)
                        streamlit.caption(f"Veracity: {score}/5 {'⭐' * score}")
                        if article.get('urlToImage'):
                            streamlit.image(article['urlToImage'], use_container_width=True)
                        else:
                            streamlit.write("📷 No image available")

                        article_key = f"article_{i}_{j}"
                        if streamlit.button("📖 Read More", key=f"btn_{article_key}", use_container_width=True):
                            streamlit.session_state[article_key] = not streamlit.session_state.get(article_key, False)

                        if streamlit.session_state.get(article_key):
                            with streamlit.expander("Full Article", expanded=True):
                                streamlit.write(f"### {article['title']}")
                                streamlit.write(article.get('description', 'No description available'))
                                streamlit.write(f"**Source:** {article['source']['name']}")
                                streamlit.write(f"[Open in Browser]({article['url']})")
