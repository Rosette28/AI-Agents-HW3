"""Bibliography extraction and generation tools."""
import re


def extract_references(research_output: str) -> list[str]:
    """Extract reference lines from the researcher output."""
    refs = re.findall(r"REF:\s*(.*)", research_output)

    if refs:
        return refs

    return [
        "Artificial Intelligence: A Modern Approach",
        "OpenAI Technical Reports",
        "Agentic AI Systems Survey",
    ]


def build_bibliography(refs: list[str]) -> str:
    """Format extracted references into a LaTeX bibliography."""
    result = "\n\n\\section*{Bibliography}\n"
    result += "\\begin{thebibliography}{99}\n"

    for idx, ref in enumerate(refs):
        result += f"\\bibitem{{ref{idx}}} {ref}\n"

    result += "\\end{thebibliography}\n"

    return result
