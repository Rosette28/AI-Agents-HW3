"""Tests for the chapter planner."""
from unittest.mock import MagicMock, patch

from src.sdk.chapter_planner import build_chapters


@patch("src.sdk.chapter_planner.Task")
def test_build_chapters_success(mock_task_class) -> None:
    """Test successful JSON extraction from planner."""
    mock_agent = MagicMock()
    mock_task_instance = MagicMock()
    # Simulate a successful JSON response from the LLM
    mock_task_instance.execute_sync.return_value.raw = '[{"title": "Chap 1", "description": "Desc", "constraint": ""}]'
    mock_task_class.return_value = mock_task_instance

    chapters = build_chapters(mock_agent, "AI")

    assert len(chapters) == 1
    assert chapters[0]["title"] == "Chap 1"

@patch("src.sdk.chapter_planner.Task")
def test_build_chapters_fallback(mock_task_class) -> None:
    """Test fallback when LLM returns invalid JSON."""
    mock_agent = MagicMock()
    mock_task_instance = MagicMock()
    # Simulate bad JSON to trigger the exception fallback
    mock_task_instance.execute_sync.return_value.raw = "I am a helpful AI. Here is some invalid text."
    mock_task_class.return_value = mock_task_instance

    chapters = build_chapters(mock_agent, "AI")

    assert len(chapters) == 8
    assert "Chapter 1" in chapters[0]["title"]
    assert "LaTeX table" in chapters[2]["constraint"]
