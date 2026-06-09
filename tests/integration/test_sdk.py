from unittest.mock import MagicMock
from unittest.mock import patch

from src.sdk.sdk import CrewPipelineSDK


@patch("src.sdk.sdk.Crew")
@patch("src.sdk.sdk.create_review_task")
@patch("src.sdk.sdk.create_writing_task")
@patch("src.sdk.sdk.create_research_task")
@patch("src.sdk.sdk.create_editor")
@patch("src.sdk.sdk.create_writer")
@patch("src.sdk.sdk.create_researcher")
def test_sdk_run(
    mock_researcher,
    mock_writer,
    mock_editor,
    mock_research_task,
    mock_writing_task,
    mock_review_task,
    mock_crew
):
    mock_researcher.return_value = MagicMock()
    mock_writer.return_value = MagicMock()
    mock_editor.return_value = MagicMock()

    mock_research_task.return_value = MagicMock()
    mock_writing_task.return_value = MagicMock()
    mock_review_task.return_value = MagicMock()

    crew_instance = MagicMock()
    crew_instance.kickoff.return_value = "SUCCESS"

    mock_crew.return_value = crew_instance

    sdk = CrewPipelineSDK()

    result = sdk.run(
        topic="Artificial Intelligence",
        language="English"
    )

    assert result == "SUCCESS"

    crew_instance.kickoff.assert_called_once()