"""Tests for the document editor."""
from unittest.mock import MagicMock, patch

from src.sdk.document_editor import edit_document


@patch("src.sdk.document_editor.Task")
def test_edit_document(mock_task_class) -> None:
    """Test the document editor function."""
    mock_agent = MagicMock()
    mock_task_instance = MagicMock()
    mock_task_instance.execute_sync.return_value.raw = "Edited Content"
    mock_task_class.return_value = mock_task_instance

    result = edit_document(mock_agent, "Raw Content")

    assert result == "Edited Content"
    mock_task_class.assert_called_once()
