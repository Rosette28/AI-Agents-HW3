"""Task definition module."""
from crewai import Agent, Task


def create_research_task(agent: Agent, topic: str) -> Task:
    """Initialize the research task."""
    return Task(
        description=(
            f"Research '{topic}'. "
            "Provide a detailed summary. "
            "Then list exactly 3 references. "
            "Each reference must start with REF:"
        ),
        expected_output="Summary plus REF lines.",
        agent=agent,
    )


def create_plan_task(agent: Agent, topic: str) -> Task:
    """Initialize the outline planning task."""
    return Task(
        description=(
            f"Create an 8 chapter plan for '{topic}'. "
            "Output ONLY JSON."
        ),
        expected_output="JSON array.",
        agent=agent,
    )
