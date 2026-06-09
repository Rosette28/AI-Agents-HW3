from crewai import Task

def create_research_task(agent):
    return Task(
        description=(
            "Research '{topic}'. Find at least 3 distinct, credible sources. "
            "CRITICAL: You MUST use the 'BibTeX Appender' tool to save each source to the bibliography."
        ),
        expected_output="A detailed research document with saved BibTeX citations.",
        agent=agent
    )

def create_writing_task(agent, research_task):
    return Task(
        description=(
            "Using the research, write an exhaustive, highly detailed academic book on '{topic}'. "
            "To meet the 15-page requirement, you must write at least 6 long chapters. "
            "CRITICAL REQUIREMENTS: "
            "1. Use the 'Dynamic Graph Generator' tool to create a graph based on your data. "
            "2. Include a native LaTeX TikZ block diagram (`\\begin{{tikzpicture}}`). "
            "3. Include a formatted data table. "
            "4. Include a complex 'fancy formula' using `\\begin{{equation}}`. "
            "5. CRITICAL: Write exactly ONE dedicated chapter that smoothly blends Hebrew and English (BiDi) to demonstrate RTL/LTR transitions."
        ),
        expected_output="A massive, highly detailed Markdown/LaTeX manuscript containing a graph, TikZ diagram, math, and a bilingual Hebrew/English chapter.",
        agent=agent,
        context=[research_task]
    )

def create_review_task(agent, writing_task):
    return Task(
        description=(
            "Review the manuscript. Ensure the \\includegraphics for the graph is present. "
            "Verify the TikZ syntax, the math formula, and ensure the BiDi Hebrew chapter is formatted correctly "
            "according to your injected SKILL.md guidelines."
        ),
        expected_output="The final, flawless LaTeX-ready text string.",
        agent=agent,
        context=[writing_task]
    )