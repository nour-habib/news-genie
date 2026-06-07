from langchain_anthropic import ChatAnthropic
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_core.prompts import ChatPromptTemplate
from models import Article

#Config
LLM = ChatAnthropic(model="claude-3-5-sonnet-20240620")

#prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are to verify news articles, making sure the user does not consume fake news."),
    ("placeholder", "{history}"),
    ("human", "{input}"),
])


memory = ConversationBufferMemory(return_message=True)

#Agent
def verification_agent():
    return ConversationChain(
        llm=LLM,
        prompt=prompt,
        memory=memory,
    )


#Run
def run(article: Article) -> str:
    agent = verification_agent()

    article_text = f"""
    Title: {article.title}
    Description: {article.description}
    Source: {article.source}
    URL: {article.url}
    """

    result = agent.invoke({"input": article_text})
    return result["response"]

    