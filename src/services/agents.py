"""Agents module for defining the AI workforce."""

import os

import crewai.llms.cache as _crewai_cache
from crewai import LLM, Agent
from dotenv import load_dotenv

from src.services.tools import web_search_tool

_crewai_cache.mark_cache_breakpoint = lambda msg: msg

load_dotenv()


def _build_llm(env_name: str, default: str) -> LLM:
    return LLM(
        model=os.getenv(env_name, default),
    )


research_llm = _build_llm(
    "RESEARCH_MODEL",
    os.getenv(
        "ACTIVE_MODEL",
        "groq/llama-3.3-70b-versatile",
    ),
)

writer_llm = _build_llm(
    "WRITER_MODEL",
    os.getenv(
        "ACTIVE_MODEL",
        "groq/llama-3.3-70b-versatile",
    ),
)

planner_llm = _build_llm(
    "PLANNER_MODEL",
    os.getenv(
        "ACTIVE_MODEL",
        "groq/llama-3.3-70b-versatile",
    ),
)

summarizer_llm = _build_llm(
    "SUMMARIZER_MODEL",
    os.getenv(
        "ACTIVE_MODEL",
        "groq/llama-3.3-70b-versatile",
    ),
)

editor_llm = _build_llm(
    "EDITOR_MODEL",
    os.getenv(
        "ACTIVE_MODEL",
        "groq/llama-3.3-70b-versatile",
    ),
)


def create_researcher() -> Agent:
    return Agent(
        role="Academic Research Analyst",
        goal="Produce factual research and references.",
        backstory="Expert academic researcher.",
        tools=[web_search_tool],
        llm=research_llm,
        verbose=True,
        allow_delegation=False,
    )


def create_writer() -> Agent:
    return Agent(
        role="Senior Academic Writer",
        goal="Write coherent academic chapters.",
        backstory="University textbook author.",
        tools=[],
        llm=writer_llm,
        verbose=True,
        allow_delegation=False,
    )


def create_editor() -> Agent:
    return Agent(
        role="LaTeX Editor",
        goal="Review academic content and fix LaTeX issues.",
        backstory="Expert LaTeX reviewer.",
        tools=[],
        llm=editor_llm,
        verbose=True,
        allow_delegation=False,
    )


def create_planner() -> Agent:
    return Agent(
        role="Academic Planner",
        goal="Create chapter structures.",
        backstory="Academic architect.",
        tools=[],
        llm=planner_llm,
        verbose=True,
        allow_delegation=False,
    )


def create_summarizer() -> Agent:
    return Agent(
        role="Context Summarizer",
        goal="Compress context efficiently.",
        backstory="Expert summarizer.",
        tools=[],
        llm=summarizer_llm,
        verbose=True,
        allow_delegation=False,
    )
