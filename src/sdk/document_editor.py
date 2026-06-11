"""Document review and editing module."""
from crewai import Agent, Task

from src.sdk.chapter_writer import _WRITER_FALLBACK_MODELS, _execute_with_rate_limit_retry


def edit_document(editor: Agent, content: str) -> str:
    """Perform a final review pass to fix minor formatting issues."""
    editor_task = Task(
        description=(
            "Review this LaTeX document.\n"
            "Fix repetition.\n"
            "Fix malformed LaTeX.\n"
            "Fix broken tables.\n"
            "Fix TikZ.\n"
            "Output ONLY LaTeX body text.\n\n"
            f"{content[:30000]}"
        ),
        expected_output="Corrected LaTeX.",
        agent=editor,
    )

    try:
        return _execute_with_rate_limit_retry(
            editor_task, editor, fallback_models=_WRITER_FALLBACK_MODELS
        )
    except Exception as e:  # noqa: BLE001
        import logging as _logging
        _logging.getLogger(__name__).warning(
            "Editor skipped (document too large or model error): %s", e
        )
        return content
