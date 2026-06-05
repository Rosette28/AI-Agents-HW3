from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from crewai.tools import tool
from src.shared.gatekeeper import ApiGatekeeper
from src.shared.config import load_config

# Initialize the gatekeeper with the configuration limits
config = load_config("rate_limits.json")
gatekeeper = ApiGatekeeper(config)

# Initialize the search wrapper (DuckDuckGo is free and part of langchain-community)
search_wrapper = DuckDuckGoSearchAPIWrapper()

def _perform_network_search(query: str) -> str:
    """The raw network call function to be passed to the gatekeeper."""
    return search_wrapper.run(query)

@tool("Web Search Tool")
def web_search_tool(query: str) -> str:
    """
    Searches the web for information on a given topic. 
    Useful for finding up-to-date facts and sources.
    """
    # Task 3.2.2: All tool execution strictly routes through ApiGatekeeper
    return gatekeeper.execute(_perform_network_search, query)