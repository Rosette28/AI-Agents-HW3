from unittest.mock import mock_open, patch

from src.services.tools import append_bibtex_tool, generate_dynamic_graph_tool, web_search_tool


@patch("src.services.tools._perform_network_search")
def test_web_search_tool_mocked(mock_search):
    # Setup the mock to return a fake search result
    mock_search.return_value = "Fake search result about AI."

    # Use .func() to test the underlying Python function directly
    result = web_search_tool.func(query="AI Agents")

    assert result == "Fake search result about AI."
    mock_search.assert_called_once_with("AI Agents")


@patch("matplotlib.pyplot.savefig")
def test_generate_dynamic_graph_tool(mock_savefig):
    # Use .func() and pass the arguments directly
    result = generate_dynamic_graph_tool.func(
        title="Test Graph",
        x_labels="A, B",
        y_values="10, 20",
    )

    assert "assets/graph.png" in result
    mock_savefig.assert_called_once()


@patch("src.services.tools.Path.open", new_callable=mock_open)
def test_append_bibtex_tool(mock_file):
    # Use .func() and pass the arguments directly
    result = append_bibtex_tool.func(
        citation_id="test2026",
        title="Test Title",
        author="John Doe",
        year="2026",
        url="http://example.com",
    )

    assert "test2026" in result
    # Notice we removed "biblio.bib" from the assert, because Path.open()
    # receives the filename via the Path object, not as a direct argument.
    mock_file.assert_called_once_with("a", encoding="utf-8")
    mock_file().write.assert_called()
