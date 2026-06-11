"""Chapter planner and outline generator."""
import json
import logging
import re

from crewai import Agent, Task

from src.sdk.chapter_writer import _WRITER_FALLBACK_MODELS, _execute_with_rate_limit_retry

logger = logging.getLogger(__name__)

def build_chapters(planner: Agent, topic: str) -> list[dict]:
    """Construct a dynamic table of contents using the planner agent."""
    plan_task = Task(
        description=(
            f"Create an 8 chapter academic outline for '{topic}'. "
            "Output ONLY valid JSON.\n"
            "Each chapter must contain:\n"
            "title\n"
            "description\n"
            "constraint\n"
            "Assign exactly one table chapter (tabularx), "
            "one equation chapter, "
            "one graph/figure chapter (using \\includegraphics{graph.png}), "
            "and one TikZ diagram chapter."
        ),
        expected_output="JSON array.",
        agent=planner,
    )

    plan_output = _execute_with_rate_limit_retry(
        plan_task, planner, fallback_models=_WRITER_FALLBACK_MODELS
    )

    try:
        json_text = re.search(
            r"\[.*\]",
            plan_output,
            re.DOTALL,
        ).group(0)

        # Escape lone backslashes that are invalid in JSON (e.g. LaTeX sequences)
        json_text = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', json_text)

        return json.loads(json_text)

    except Exception as e:  # noqa: BLE001
        logger.warning("Falling back to default outline due to error: %s", e)

        chapters = [
            {
                "title": f"Chapter {i+1}",
                "description": "Discuss thoroughly.",
                "constraint": "",
            }
            for i in range(8)
        ]

        chapters[2]["constraint"] = "Include a LaTeX table (use tabularx with X columns so it fits the page width)."
        chapters[4]["constraint"] = "Include a LaTeX math equation block."
        chapters[5]["constraint"] = r"Include a bar-chart figure using \includegraphics[width=0.8\textwidth]{graph.png} inside a \begin{figure}[htbp] environment with a Hebrew caption."
        chapters[6]["constraint"] = "Include a LaTeX TikZ diagram with Hebrew node labels."

        return chapters
