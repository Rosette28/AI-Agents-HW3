"""SDK module for the CrewAI pipeline."""
import logging

from crewai import Task

from src.sdk.bibliography import (
    build_bibliography,
    extract_references,
)
from src.sdk.chapter_writer import _WRITER_FALLBACK_MODELS, _execute_with_rate_limit_retry
from src.sdk.pipeline_helpers import (
    build_chapters,
    edit_document,
    write_document,
)
from src.services.agents import (
    create_editor,
    create_planner,
    create_researcher,
    create_summarizer,
    create_writer,
)

logger = logging.getLogger(__name__)


class CrewPipelineSDK:
    """Core SDK for managing the document generation pipeline."""

    def __init__(self) -> None:
        """Initialize all required agents."""
        self.researcher = create_researcher()
        self.planner = create_planner()
        self.summarizer = create_summarizer()
        self.writer = create_writer()
        self.editor = create_editor()

    def run(
        self,
        topic: str,
        language: str,
        cover_sheet: dict | None = None,
    ) -> str:
        """Run the end-to-end multi-agent pipeline."""
        if cover_sheet:
            logger.info("Cover sheet received.")

        logger.info("Starting research phase...")

        research_task = Task(
            description=(
                f"Research '{topic}'. "
                "Provide a detailed summary. "
                "Then list exactly 3 references. "
                "Each reference must begin with REF:"
            ),
            expected_output="Summary and references.",
            agent=self.researcher,
        )

        research_output = _execute_with_rate_limit_retry(
            research_task, self.researcher, fallback_models=_WRITER_FALLBACK_MODELS
        )

        logger.info("Planning outline...")

        chapters = build_chapters(
            self.planner,
            topic,
        )

        logger.info("Writing chapters...")

        full_content = write_document(
            writer=self.writer,
            summarizer=self.summarizer,
            topic=topic,
            language=language,
            chapters=chapters,
        )

        logger.info("Running editor...")

        final_content = edit_document(
            self.editor,
            full_content,
        )

        refs = extract_references(
            research_output,
        )

        final_content += build_bibliography(
            refs,
        )

        return final_content
