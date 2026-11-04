
from dotenv import load_dotenv
from langchain import messages
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from tavily import TavilyClient

load_dotenv()

tavily = TavilyClient()

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

llm = ChatOllama(model="qwen3:4b")
tools = [search]
agent = create_agent(model=llm, tools=tools)


def main() -> None:
    print("Hello from langchain-course!")
    result = agent.invoke({"messages": HumanMessage(content="Share 3 job openings for AI application engineer who knows LangChain and LangGraph in India")})
    print(result)

if(__name__ == "__main__"):
    main()