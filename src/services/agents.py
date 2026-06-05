from crewai import Agent
from src.services.tools import web_search_tool

def create_researcher() -> Agent:
    return Agent(
        role="Market Research Analyst",
        goal="Find accurate, up-to-date information and credible sources on {topic}.",
        backstory=(
            "You are a meticulous research analyst. You navigate complex data "
            "landscapes to find credible sources, extracting key facts and figures "
            "without hallucinating information."
        ),
        tools=[web_search_tool],
        verbose=True,
        allow_delegation=False
    )

def create_writer() -> Agent:
    return Agent(
        role="Senior Technical Writer",
        goal=(
            "Turn research material into a clear, well-structured academic article "
            "written strictly in the requested language mode: {language}."
        ),
        backstory=(
            "You transform raw research into accessible, academic Markdown prose. "
            "You are an expert at structuring chapters and adapting your writing "
            "perfectly to the user-selected language, ensuring smooth readability."
        ),
        verbose=True,
        allow_delegation=False
    )

def create_editor() -> Agent:
    return Agent(
        role="Senior Editor",
        goal=(
            "Check factual accuracy against the research, improve structural clarity, "
            "and format the final output ensuring absolute readiness for LaTeX compilation."
        ),
        backstory=(
            "You review drafts meticulously. You never change the original factual meaning. "
            "Your expertise lies in ensuring that Markdown tables, lists, and formatting "
            "are perfectly standardized so the LaTeX compiler can digest them seamlessly."
        ),
        verbose=True,
        allow_delegation=False
    )

