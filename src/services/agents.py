import os

from dotenv import load_dotenv
from crewai import Agent, LLM

from src.services.tools import web_search_tool

load_dotenv()

gemini_llm = LLM(
    model="gemini/gemini-1.5-pro",
    api_key=os.getenv("GEMINI_API_KEY")
)


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
        llm=gemini_llm,
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
        llm=gemini_llm,
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
        llm=gemini_llm,
        verbose=True,
        allow_delegation=False
    )