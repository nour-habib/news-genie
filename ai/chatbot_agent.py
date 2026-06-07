from langchain_anthropic import ChatAnthropic
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_core.prompts import ChatPromptTemplate


#Config
LLM = ChatAnthropic(model="claude-3-5-sonnet-20240620")

#Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a chatbot assistance for a news platform."),
    ("placeholder", "{history}"),
    ("human", "{input}"),
])


memory = ConversationBufferMemory(return_message=True)


#Agent
def chatbot():
    return ConversationChain(
        llm=LLM,
        prompt=prompt,
        memory=memory,
    )


#Run
def run(query: str) -> str:
    agent = chatbot()
    result = agent.invoke({"input": query})
    result result["response"]