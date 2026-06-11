"""Unit tests for agents and tasks."""
from src.services.agents import (
    create_editor,
    create_researcher,
    create_writer,
)


def test_agent_creation() -> None:
    """Test agent role assignments."""
    researcher = create_researcher()
    writer = create_writer()
    editor = create_editor()

    assert researcher.role == "Academic Research Analyst"
    assert writer.role == "Senior Academic Writer"
    assert editor.role == "LaTeX Editor"
