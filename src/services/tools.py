import os
import matplotlib.pyplot as plt
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from crewai.tools import tool
from src.shared.gatekeeper import ApiGatekeeper
from src.shared.config import load_config

config = load_config("rate_limits.json")
gatekeeper = ApiGatekeeper(config)
search_wrapper = DuckDuckGoSearchAPIWrapper()

def _perform_network_search(query: str) -> str:
    return search_wrapper.run(query)

@tool("Web Search Tool")
def web_search_tool(query: str) -> str:
    """Searches the web for up-to-date facts and sources."""
    return gatekeeper.execute(_perform_network_search, query)

@tool("Dynamic Graph Generator")
def generate_dynamic_graph_tool(title: str, x_labels: str, y_values: str) -> str:
    """
    Generates a bar chart and saves it. 
    Provide x_labels as a comma-separated string (e.g., "A,B,C") 
    and y_values as a comma-separated string of numbers (e.g., "10,20,30").
    """
    os.makedirs('assets', exist_ok=True)
    labels = [x.strip() for x in x_labels.split(',')]
    values = [float(y.strip()) for y in y_values.split(',')]
    
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['#4C72B0', '#55A868', '#C44E52'])
    plt.title(title)
    plt.ylabel('Value')
    plt.savefig('assets/graph.png', bbox_inches='tight')
    plt.close()
    return "Graph successfully saved to assets/graph.png. Use \\includegraphics{assets/graph.png} in the text."

@tool("BibTeX Appender")
def append_bibtex_tool(citation_id: str, title: str, author: str, year: str, url: str) -> str:
    """
    Formats a source into BibTeX and appends it to biblio.bib.
    Use this for every credible source found.
    """
    bibtex_entry = f"""
@misc{{{citation_id},
  title={{{title}}},
  author={{{author}}},
  year={{{year}}},
  howpublished={{\\url{{{url}}}}}
}}
"""
    with open("biblio.bib", "a", encoding="utf-8") as f:
        f.write(bibtex_entry)
    return f"Source {citation_id} added to bibliography. Cite it using \cite{{{citation_id}}}."