import os

from crewai import LLM, Agent
from dotenv import load_dotenv

from src.services.tools import append_bibtex_tool, generate_dynamic_graph_tool, web_search_tool

load_dotenv()
gemini_llm = LLM(model="gemini/gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY"))

def create_researcher() -> Agent:
    return Agent(
        role="Market Research Analyst",
        goal="Find accurate facts on {topic}. Use the BibTeX Appender tool to save every source you find.",
        backstory="You find credible sources and immediately save them to the bibliography using your tools.",
        tools=[web_search_tool, append_bibtex_tool],
        llm=gemini_llm,
        verbose=True,
        allow_delegation=False,
    )

def create_writer() -> Agent:
    return Agent(
        role="Senior Technical Writer",
        goal="Write a massive 15-page academic article in {language}. You must generate a graph using your tool.",
        backstory="You are an expansive academic writer. You never write short summaries. You expand on every point to ensure the document reaches approximately 15 pages.",
        tools=[generate_dynamic_graph_tool],
        llm=gemini_llm,
        verbose=True,
        allow_delegation=False,
    )

def create_editor() -> Agent:
    return Agent(
        role="Senior Editor",
        goal="Format the output for LaTeX compilation based on your injected academic skills.",
        backstory="You strictly enforce LaTeX syntax. You ensure TikZ block diagrams, tables, and complex math equations are perfectly formatted.",
        llm=gemini_llm,
        skills=["./skills"], # Appendix A: Injecting the Skill folder
        verbose=True,
        allow_delegation=False,
    )
