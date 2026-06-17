from langgraph.graph import StateGraph, END, START
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict, Literal
from dotenv import load_dotenv

load_dotenv()


def verify_articles(articles: list) -> list:
    """Determine veracity of each article and score from 1-5."""
    from ai.agents.verification_agent import run as verify

    for article in articles:
        try:
            from ai.models.article import Article
            article_obj = Article(
                title=article.get('title', ''),
                description=article.get('description') or '',
                source=article.get('source', {}).get('name', 'Unknown'),
                url=article.get('url', '')
            )
            # Get veracity score
            article['veracity_score'] = verify(article_obj)
        except Exception as e:
            print(f"Error verifying article: {e}")
            article['veracity_score'] = 3  # Default to neutral

    return articles 

class RouterState(TypedDict):
    user_query: str
    query_type: Literal["news", "general"]
    response: str


llm = ChatOpenAI(model="gpt-4o", temperature=0.7)


def classify_query(state: RouterState) -> RouterState:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Classify user input as either 'news' or 'general'.

NEWS: Requests for articles, headlines, or current events (e.g., "Show me latest tech news", "Top stories about crypto", "What's happening in finance")
GENERAL: Specific questions, definitions, facts, or how-tos (e.g., "Who won the World Cup?", "How does AI work?", "What's quantum computing?")

Return only the word: 'news' or 'general'"""),
        ("human", "{input}")
    ])

    chain = prompt | llm
    result = chain.invoke({"input": state["user_query"]})
    query_type = result.content.strip().lower()

    return {
        **state,
        "query_type": "news" if "news" in query_type else "general"
    }


def route_to_chatbot(state: RouterState) -> RouterState:
    from ai.agents.chatbot_agent import run as chatbot_run
    response = chatbot_run(state["user_query"], state["query_type"])
    
    return {**state, "response": response}


def build_router():
    graph = StateGraph(RouterState)

    graph.add_node("classify", classify_query)
    graph.add_node("chatbot", route_to_chatbot)

    graph.add_edge(START, "classify")
    graph.add_edge("classify", "chatbot")
    graph.add_edge("chatbot", END)

    return graph.compile()


router = build_router()


def run_query(user_input: str) -> str:
    result = router.invoke({
        "user_query": user_input,
        "query_type": "",
        "response": ""
    })
    return result["response"]
