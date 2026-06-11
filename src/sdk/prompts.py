"""Prompt builders for the AI agents."""
import json


def build_language_rule(language: str) -> str:
    """Build the language specific constraint string."""
    if language.lower() == "bidi":
        return """
LANGUAGE: Write EXCLUSIVELY in Hebrew.

CRITICAL RULES:
- Every sentence, heading, and paragraph body MUST be in Hebrew.
- Technical terms may appear in English ONCE in parentheses when first introduced.
- ABSOLUTELY NO other languages: no Chinese, no Korean, no Thai, no Arabic, no Russian, no Vietnamese, no Japanese.
- Even a single word in a forbidden language will cause the document to fail.

Example of CORRECT usage:
בינה מלאכותית כללית (Artificial General Intelligence, AGI) היא...

After the first introduction, use the Hebrew term only.
"""
    return "Write in English."


def build_writer_prompt(
    topic: str,
    chapter: dict,
    outline: list,
    summary: str,
    language_rule: str,
) -> str:
    """Construct the main text generation prompt."""
    return f"""
You are writing a university-level textbook.

TOPIC:
{topic}

FULL OUTLINE:
{json.dumps(outline, ensure_ascii=False)}

PREVIOUS CHAPTER SUMMARY:
{summary}

CURRENT CHAPTER:
{chapter["title"]}

FOCUS:
{chapter["description"]}

CONSTRAINT:
{chapter.get("constraint", "")}

{language_rule}

REQUIREMENTS:

- Minimum 800 words.
- Complete paragraphs only.
- Every paragraph must contain at least 3 sentences.
- No keyword lists.
- No acronym repetition.
- No filler text.
- Use academic tone.
- Use \\section and \\subsection.
- Output ONLY LaTeX body text. No \\begin{{document}}, no preamble, no \\documentclass.
- If your CONSTRAINT asks for a graph, include exactly: \\includegraphics[width=0.8\\textwidth]{{graph.png}}
- Cite sources using \\cite{{key}}. Available keys: russell2016, sutton2018, mnih2015, bhatt2022, AgenticAI2024, AgenticAI2025a, AgenticAI2025b, stanford_ai, mit_press_ai, harvard_ai, ieee_ai, agentic_ai_1, agentic_ai_2, agentic_ai_3, agentic_ai_survey
- Do NOT write \\begin{{thebibliography}} — the bibliography is generated automatically.
"""
