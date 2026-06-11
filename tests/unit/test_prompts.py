"""Unit tests for prompt generation."""
from src.sdk.prompts import build_language_rule, build_writer_prompt


def test_build_language_rule() -> None:
    """Verify language instructions generation."""
    hebrew_rule = build_language_rule("bidi")
    english_rule = build_language_rule("english")

    assert "Write entirely in Hebrew." in hebrew_rule
    assert "Write in English." in english_rule


def test_build_writer_prompt() -> None:
    """Verify writer instruction assembly."""
    outline = [{"title": "Ch1"}]
    prompt = build_writer_prompt(
        topic="AI",
        chapter={"title": "Introduction", "description": "Intro", "constraint": "table"},
        outline=outline,
        summary="Summary text",
        language_rule="Hebrew rule",
    )

    assert "TOPIC:\nAI" in prompt
    assert "CURRENT CHAPTER:\nIntroduction" in prompt
    assert "Hebrew rule" in prompt
    assert "table" in prompt
