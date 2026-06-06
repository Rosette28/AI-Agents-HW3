from crewai import Task


def create_research_task(agent):
    return Task(
        description=(
            "Research the topic '{topic}' and gather accurate facts, "
            "statistics, examples, and credible sources. "
            "The output language should support {language}."
        ),
        expected_output=(
            "A structured list of key facts, insights, and sources."
        ),
        agent=agent
    )


def create_writing_task(agent, research_task):
    return Task(
        description=(
            "Transform the research into a well-structured academic "
            "Markdown article written in {language}."
        ),
        expected_output=(
            "A complete Markdown draft organized into sections and chapters."
        ),
        agent=agent,
        context=[research_task]
    )


def create_review_task(agent, writing_task):
    return Task(
        description=(
            "Review the article for factual accuracy, clarity, and "
            "LaTeX compatibility."
        ),
        expected_output=(
            "A polished Markdown article ready for LaTeX conversion."
        ),
        agent=agent,
        context=[writing_task]
    )