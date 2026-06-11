"""Main entry point for the Agentic AI Research Pipeline."""
import logging
import shutil
import subprocess
from pathlib import Path

from src.sdk.sanitizer import guarantee_graph_exists, sanitize_to_latex_body
from src.sdk.sdk import CrewPipelineSDK
from src.services.latex_builder import generate_latex_document

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main() -> None:
    """Execute the main application pipeline."""
    topic = input("Enter topic: ")
    language = input("Enter language (english/bidi): ")
    author = input("Author (optional): ")
    date = input("Date (optional): ")
    course = input("Course (optional): ")
    lecturer = input("Lecturer (optional): ")

    cover_sheet = {
        "author": author,
        "date": date,
        "course": course,
        "lecturer": lecturer,
    }

    sdk = CrewPipelineSDK()
    logger.info("Starting generation process...")
    raw_content = sdk.run(topic=topic, language=language, cover_sheet=cover_sheet)

    logger.info("Agents finished writing! Sanitizing LaTeX output...")
    clean_content = sanitize_to_latex_body(raw_content)

    final_latex_string = generate_latex_document(
        topic=topic,
        language=language,
        content=clean_content,
        cover_sheet=cover_sheet,
    )

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    tex_path = output_dir / "document.tex"
    with tex_path.open("w", encoding="utf-8") as f:
        f.write(final_latex_string)

    guarantee_graph_exists()

    bib_src = Path("biblio.bib")
    if bib_src.exists():
        shutil.copy(bib_src, output_dir / "biblio.bib")

    logger.info("Running LuaLaTeX compiler (pass 1)...")
    subprocess.run(["lualatex", "-interaction=nonstopmode", "-output-directory=output", "output/document.tex"], check=False)  # noqa: S607
    logger.info("Running Biber for bibliography...")
    subprocess.run(["biber", "output/document"], check=False)  # noqa: S607
    logger.info("Running LuaLaTeX compiler (pass 2)...")
    subprocess.run(["lualatex", "-interaction=nonstopmode", "-output-directory=output", "output/document.tex"], check=False)  # noqa: S607
    logger.info("Running LuaLaTeX compiler (pass 3)...")
    subprocess.run(["lualatex", "-interaction=nonstopmode", "-output-directory=output", "output/document.tex"], check=False)  # noqa: S607
    pdf_path = output_dir / "document.pdf"
    if pdf_path.exists():
        logger.info("SUCCESS! Your PDF has been generated at: output/document.pdf")
    else:
        logger.error("ERROR: LuaLaTeX compilation failed. Check output/document.log.")


if __name__ == "__main__":
    main()
