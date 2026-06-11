"""Tests for text validators."""
from src.sdk.validators import is_invalid_text


def test_invalid_text_too_short() -> None:
    """Test that short text is rejected."""
    assert is_invalid_text("Too short") is True

def test_invalid_text_collapse() -> None:
    """Test that repetitive text is rejected."""
    text = "the " * 10 + "a b c d e f g h i j"
    assert is_invalid_text(text) is True

def test_valid_text() -> None:
    """Test that valid text passes."""
    text = " ".join([f"word{i}" for i in range(160)])
    assert is_invalid_text(text) is False
