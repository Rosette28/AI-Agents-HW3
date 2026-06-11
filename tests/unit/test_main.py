"""Tests for the main application entry point."""
from unittest.mock import patch

import src.main


@patch("src.main.input", side_effect=["Agentic AI", "english", "Author", "Date", "Course", "Lecturer"])
@patch("src.main.CrewPipelineSDK")
@patch("src.main.subprocess.run")
def test_main_execution(mock_run, mock_sdk, mock_input) -> None:  # noqa: ARG001
    """Verify full main function execution path."""
    mock_instance = mock_sdk.return_value
    mock_instance.run.return_value = "\\begin{document}\nTest Content\n\\end{document}"

    src.main.main()

    mock_instance.run.assert_called_once()
    mock_run.assert_called()
