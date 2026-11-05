
from typing import List

from dotenv import load_dotenv
from langchain import messages
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field
from tavily import TavilyClient

load_dotenv()

tavily = TavilyClient()

class Source(BaseModel):
    """Schema for source used by Agent"""

    url: str = Field(description="The url of the source")

class AgentResponse(BaseModel):
    """Schema for Agent response with answer and sources"""

    answer: str = Field(description="Answer from the agent for the query")
    sources: List[Source] = Field(default_factory=list, description="List of sources used to generate the answer")

@tool
def search(query: str) -> str:
    """
    Tool that searches over internet
    Args:
        query: What to search for
    Returns:
        The search result
    """
    print(f"Searching for {query}")
    return tavily.search(query=query)

llm = ChatOllama(model="gpt-oss:20b")
tools = [search]
agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)


def main() -> None:
    print("Hello from langchain-course!")
    result = agent.invoke({"messages": HumanMessage(content="Share 3 job openings for AI application engineer in Product based companies who knows LangChain and LangGraph in India and have 6 years of Software engineeing experience")})
    print(result)

if(__name__ == "__main__"):
    main()