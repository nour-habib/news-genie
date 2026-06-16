from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ai.models.article import Article
from dotenv import load_dotenv

load_dotenv()

#Config
LLM = ChatOpenAI(model="gpt-4o", temperature=0.7)


#Run
def run(article: Article) -> int:
    """Verify article and return veracity score (1-5)."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a fact-checker. Rate the veracity of this article from 1-5 where 1=fake/misinformation and 5=trustworthy. Respond with ONLY the number."),
        ("human", "{article_text}")
    ])

    chain = prompt | LLM

    article_text = f"""Title: {article.title}
Description: {article.description}
Source: {article.source}
URL: {article.url}"""

    result = chain.invoke({"article_text": article_text})
    try:
        score = int(result.content.strip())
        return max(1, min(5, score))
    except:
        return 3

    