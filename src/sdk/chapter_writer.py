"""Chapter drafting and iterative writing module."""
import logging
import re
import time

from crewai import Agent, Task

from src.sdk.prompts import build_language_rule, build_writer_prompt
from src.sdk.validators import is_invalid_text

logger = logging.getLogger(__name__)

_RATE_LIMIT_DEFAULT_WAIT = 120

# Fallback models tried in order (best → worst) when the primary hits rate/daily limits.
_WRITER_FALLBACK_MODELS = [
    "groq/openai/gpt-oss-120b",                               # intelligence 33.27 — best on Groq
    "groq/openai/gpt-oss-20b",                                # intelligence 24.47
    "groq/meta-llama/llama-4-maverick-17b-128e-instruct",     # Llama 4 MoE
    "groq/meta-llama/llama-4-scout-17b-16e-instruct",         # Llama 4 Scout
    "groq/qwen/qwen3-32b",                                    # Qwen3 32B
    "groq/llama3-70b-8192",                                   # Llama 3 70B (legacy)
    "groq/llama-3.1-8b-instant",                              # last resort
]


def _execute_with_rate_limit_retry(
    task: Task,
    agent: Agent,
    fallback_models: list[str] | None = None,
) -> str:
    """Execute a task and retry automatically if a rate limit error occurs.

    When the daily token limit (TPD) is hit and fallback_models are provided,
    the agent's model is switched to the next fallback instead of waiting.
    """
    remaining = list(fallback_models) if fallback_models else []

    while True:
        try:
            return task.execute_sync(agent=agent).raw
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            # Model decommissioned — skip to next fallback immediately
            if ("model_decommissioned" in msg or "has been decommissioned" in msg) and remaining:
                next_model = remaining.pop(0)
                logger.warning("Model decommissioned. Switching to: %s", next_model)
                agent.llm.model = next_model
                continue
            if "rate_limit_exceeded" in msg or "RateLimitError" in msg:
                if "Request too large" in msg or "please reduce your message size" in msg:
                    raise
                # Daily limit hit — switch to a fallback model if available
                if "tokens per day" in msg and remaining:
                    next_model = remaining.pop(0)
                    logger.warning(
                        "Daily token limit hit. Switching model to: %s", next_model
                    )
                    agent.llm.model = next_model
                    continue
                match = re.search(r"try again in (\d+)m(\d+(?:\.\d+)?)s", msg)
                if match:
                    wait = int(match.group(1)) * 60 + float(match.group(2)) + 5
                else:
                    match = re.search(r"try again in (\d+(?:\.\d+)?)s", msg)
                    wait = float(match.group(1)) + 5 if match else _RATE_LIMIT_DEFAULT_WAIT
                logger.warning("Rate limit hit. Waiting %.0f seconds...", wait)
                time.sleep(wait)
            else:
                raise


def write_document(
    writer: Agent,
    summarizer: Agent,
    topic: str,
    language: str,
    chapters: list[dict],
) -> str:
    """Iterate over the outline to write and summarize each chapter."""
    language_rule = build_language_rule(language)

    full_content = ""
    rolling_summary = "No previous chapters."

    outline_titles = [chapter["title"] for chapter in chapters]

    for index, chapter in enumerate(chapters):
        logger.info("Writing chapter %d: %s", index + 1, chapter["title"])

        prompt = build_writer_prompt(
            topic=topic,
            chapter=chapter,
            outline=outline_titles,
            summary=rolling_summary,
            language_rule=language_rule,
        )

        chapter_text = ""

        for _ in range(2):
            write_task = Task(
                description=prompt,
                expected_output="Academic LaTeX text.",
                agent=writer,
            )

            chapter_text = _execute_with_rate_limit_retry(
                write_task, writer, fallback_models=_WRITER_FALLBACK_MODELS
            )

            if not is_invalid_text(chapter_text):
                break

        full_content += (
            f"\n\n"
            f"% --- CHAPTER {index + 1} ---\n"
            f"{chapter_text}\n"
        )

        if index < len(chapters) - 1:
            summary_task = Task(
                description=(
                    "Summarize this chapter "
                    "in 3 sentences:\n\n"
                    f"{chapter_text[:2000]}"
                ),
                expected_output="Short summary.",
                agent=summarizer,
            )

            rolling_summary = _execute_with_rate_limit_retry(summary_task, summarizer)

        time.sleep(25)

    return full_content
