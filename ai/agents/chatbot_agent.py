from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0.7)


def run(user_query: str, query_type: str) -> str:
    """
    Handle both news and general queries.
    """
    print(f"DEBUG chatbot_agent: query_type='{query_type}', user_query='{user_query}'")
    if query_type == "news":
        print("DEBUG: Routing to news handler")
        return handle_news_query(user_query)
    else:
        print("DEBUG: Routing to general handler with web search")
        return handle_general_query(user_query)


def handle_news_query(user_query: str) -> str:
    """Handle news-related queries."""
    from ui.services.news_service import get_articles, verify_articles
    from ai.tools.search_tool import web_search

    # Extract category from query
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract news category from: technology, finance, sports, general, science, politics. Return only the word."),
        ("human", "{input}")
    ])

    chain = prompt | llm
    result = chain.invoke({"input": user_query})
    category = result.content.strip().lower()

    category_map = {
        "technology": "technology",
        "finance": "business",
        "sports": "sports",
        "science": "science",
        "politics": "general",
    }

    api_category = category_map.get(category, "general")
    data = get_articles(api_category)
    articles = data.get("articles", [])

    # If no articles found, fall back to web search
    if not articles:
        print(f"DEBUG: No articles found for {api_category}, using web search instead")
        search_results = web_search.invoke({"query": user_query})
        return f"No articles found in news API. Web search results:\n\n{search_results}"

    # Verify articles
    articles = verify_articles(articles)

    # Build response with links and scores
    response = f"Found {len(articles)} articles about {api_category}:\n"
    for article in articles[:3]:
        score = article.get('veracity_score', 3)
        response += f"\n• [{article['title']}]({article['url']})\n  Source: {article['source']['name']} | Veracity: {score}/5\n"

    return response


def handle_general_query(user_query: str) -> str:
    """Handle general knowledge queries with web search."""
    from ai.tools.search_tool import web_search

    # Search the web for current information
    print(f"DEBUG: Calling web_search for: {user_query}")
    search_results = web_search.invoke({"query": user_query})
    print(f"DEBUG: Search results: {search_results}")

    # Have the LLM synthesize an answer using search results
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use the provided search results to answer the user's question concisely. If search results are available, cite sources."),
        ("human", "Question: {query}\n\nSearch Results:\n{search_results}")
    ])

    chain = prompt | llm
    result = chain.invoke({"query": user_query, "search_results": search_results})

    return result.content
