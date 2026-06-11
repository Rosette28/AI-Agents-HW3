"""Unit tests for task creation."""
from crewai import Agent

from src.services.tasks import create_plan_task, create_research_task


def test_create_research_task() -> None:
    """Ensure research task initializes correctly."""
    agent = Agent(role="R", goal="G", backstory="B")
    task = create_research_task(agent, "Agentic AI")

    assert "Research 'Agentic AI'" in task.description
    assert task.agent == agent


def test_create_plan_task() -> None:
    """Ensure plan task initializes correctly."""
    agent = Agent(role="P", goal="G", backstory="B")
    task = create_plan_task(agent, "Agentic AI")

    assert "8 chapter plan" in task.description
    assert task.agent == agent
