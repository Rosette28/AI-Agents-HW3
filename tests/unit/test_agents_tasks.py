from src.services.agents import create_editor, create_researcher, create_writer
from src.services.tasks import create_research_task, create_review_task, create_writing_task


def test_agent_and_task_initialization():
    # Test that Agents initialize correctly
    researcher = create_researcher()
    writer = create_writer()
    editor = create_editor()

    assert researcher.role == "Market Research Analyst"
    assert writer.role == "Senior Technical Writer"
    assert editor.role == "Senior Editor"

    # Test that Tasks initialize and link to the correct agents
    t_research = create_research_task(researcher)
    t_write = create_writing_task(writer, t_research)
    t_review = create_review_task(editor, t_write)

    assert t_research.agent == researcher
    assert t_write.agent == writer
    assert t_review.agent == editor
