"""Tests for bibliography generation."""
from src.sdk.bibliography import build_bibliography, extract_references


def test_extract_references_found() -> None:
    """Test extracting references via regex."""
    res = "Some text.\nREF: First ref\nREF: Second ref"
    refs = extract_references(res)
    assert refs == ["First ref", "Second ref"]

def test_extract_references_fallback() -> None:
    """Test fallback when no references are found."""
    res = "No refs here."
    refs = extract_references(res)
    assert len(refs) == 3
    assert "Artificial Intelligence: A Modern Approach" in refs

def test_build_bibliography() -> None:
    """Test LaTeX bibliography formatting."""
    refs = ["Ref 1"]
    bib = build_bibliography(refs)
    assert "\\begin{thebibliography}" in bib
    assert "\\bibitem{ref0} Ref 1" in bib
