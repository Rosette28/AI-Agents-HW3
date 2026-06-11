"""LaTeX sanitization utilities for AI-generated content."""
import logging
import re
from pathlib import Path

import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

_FALLBACK_TIKZ = (
    "\n\n\\begin{figure}[H]\n\\centering\n"
    "\\begin{tikzpicture}[node distance=2cm]\n"
    "  \\node[draw,rectangle,rounded corners,minimum width=4cm,minimum height=1cm]"
    " (perception) {Perception};\n"
    "  \\node[draw,rectangle,rounded corners,minimum width=4cm,minimum height=1cm,"
    "below of=perception] (reasoning) {Reasoning};\n"
    "  \\node[draw,rectangle,rounded corners,minimum width=4cm,minimum height=1cm,"
    "below of=reasoning] (action) {Action};\n"
    "  \\draw[->] (perception) -- (reasoning);\n"
    "  \\draw[->] (reasoning) -- (action);\n"
    "\\end{tikzpicture}\n"
    "\\caption{Agentic AI Architecture}\n"
    "\\end{figure}\n\n"
)


def _strip_foreign_chars(text: str) -> str:
    """Normalize typographic chars and strip anything outside Hebrew+ASCII."""
    for old, new in [('\u201c', "``"), ('\u201d', "''"), ('\u2018', "`"), ('\u2019', "'"),  # noqa: E501
                     ('\u2014', "---"), ('\u2013', "--"), ('\u2026', "..."), ('\u2022', r"\textbullet ")]:  # noqa: E501
        text = text.replace(old, new)
    return re.sub(r"[^\x00-\x7F\u0590-\u05FF\uFB1D-\uFB4F]", "", text)


def _close_unclosed_tabulars(text: str) -> str:
    """Close unclosed tabular environments by truncating at the last complete row."""
    for _ in range(10):
        begin_matches = list(re.finditer(r"\\begin\{(tabular[x*]?)\}", text))
        end_matches = list(re.finditer(r"\\end\{(tabular[x*]?)\}", text))

        if len(begin_matches) <= len(end_matches):
            break

        closed = False
        for bm in reversed(begin_matches):
            if any(em.start() > bm.start() for em in end_matches):
                continue

            env_name = bm.group(1)
            next_marker = re.search(r"(?:\\section|\\chapter|% ---)", text[bm.start() + 1:])
            territory_end = (bm.start() + 1 + next_marker.start()) if next_marker else len(text)

            segment = text[bm.start(): territory_end]
            last_row_match = None
            for rm in re.finditer(r"\\\\[ \t]*\r?\n?", segment):
                last_row_match = rm

            if last_row_match:
                cut_point = bm.start() + last_row_match.end()
                close_str = "\n\\hline\n\\end{" + env_name + "}\n\\end{table}\n"
                text = text[:cut_point] + close_str + text[territory_end:]
            else:
                text = text[:bm.start()] + text[territory_end:]

            closed = True
            break

        if not closed:
            break
    return text

def sanitize_to_latex_body(text: str) -> str:
    """Safely cleans AI-generated LaTeX and prevents font crashing."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"%\s*Cover Template.*?\\vfill", "", text, flags=re.DOTALL)

    matches = re.findall(r"\\begin\{document\}(.*?)\\end\{document\}", text, flags=re.DOTALL)
    if matches:
        text = "\n\n".join(matches)

    # Strip manually written bibliography — biblatex handles it via \printbibliography
    text = re.sub(r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}", "", text, flags=re.DOTALL)

    bad_tags = [
        r"\\maketitle", r"\\tableofcontents",
        r"\\begin\{titlepage\}", r"\\end\{titlepage\}",
        r"\\documentclass(?:\[[^\]]*\])?\{[^}]*\}",
        r"\\usepackage(?:\[[^\]]*\])?\{[^}]*\}",
        r"\\begin\{hebrewnumbering\}", r"\\end\{hebrewnumbering\}",
        r"\\begin\{hebrew\}", r"\\end\{hebrew\}",
        r"\\begin\{english\}", r"\\end\{english\}",
    ]
    for pattern in bad_tags:
        text = re.sub(pattern, "", text)

    # Force exact figure/table placement with [H] (float package required)
    text = text.replace("[h!]", "[H]")
    text = text.replace("[h]", "[H]")
    text = text.replace("[htbp]", "[H]")
    text = text.replace(r"\chapter", r"\section")
    text = re.sub(r"\\([A-Z][A-Za-z]+)", r"\1", text)

    # Normalize all includegraphics to use our placeholder graph
    text = re.sub(r"\\includegraphics\[.*?\]\{.*?\}", r"\\includegraphics[width=0.8\\textwidth]{graph.png}", text)
    text = re.sub(r"\\includegraphics\{.*?\}", r"\\includegraphics[width=0.8\\textwidth]{graph.png}", text)

    text = _strip_foreign_chars(text)
    text = re.sub(r"\\(?:sub)*section\*?\{\s*\}", "", text)
    text = _close_unclosed_tabulars(text)

    # Wrap tables in adjustbox (prevents overflow) and reduce font size
    text = re.sub(
        r"(\\begin\{tabular[x*]?\})",
        r"\\begin{adjustbox}{max width=\\textwidth}\n\\small\n\1",
        text,
    )
    text = re.sub(r"(\\end\{tabular[x*]?\})", r"\1\n\\end{adjustbox}", text)

    if r"\includegraphics" not in text:
        text += ("\n\n\\begin{figure}[H]\n\\centering\n"
                 "\\includegraphics[width=0.8\\textwidth]{graph.png}\n"
                 "\\caption{ביצועי בינה מלאכותית אגנטית לפי תחום}\n\\end{figure}\n\n")

    if r"\begin{tikzpicture}" not in text:
        text = text + _FALLBACK_TIKZ

    # Wrap every TikZ diagram in LTR context so coordinates/arrows render correctly
    text = re.sub(r"(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})",
                  r"\\begin{otherlanguage}{english}\n\1\n\\end{otherlanguage}", text, flags=re.DOTALL)

    return text.strip()


def guarantee_graph_exists() -> None:
    """Ensure the fallback graph exists before compilation."""
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    graph_path = output_dir / "graph.png"
    if not graph_path.exists():
        categories = ["Healthcare", "Finance", "Transportation"]
        performance = [80, 70, 90]
        plt.figure(figsize=(8, 5))
        plt.bar(categories, performance, color=["blue", "green", "orange"])
        plt.title("Agentic AI Performance by Industry")
        plt.ylabel("Performance Score")
        plt.ylim(0, 100)
        plt.tight_layout()
        plt.savefig(graph_path)
        plt.close()
