from crewai import Crew, Process

from src.services.agents import create_editor, create_researcher, create_writer
from src.services.tasks import create_research_task, create_review_task, create_writing_task


class CrewPipelineSDK:
    def __init__(self):
        self.researcher = create_researcher()
        self.writer = create_writer()
        self.editor = create_editor()

    def run(
        self,
        topic,
        language,
        cover_sheet=None,
    ):
        research_task = create_research_task(
            self.researcher,
        )

        writing_task = create_writing_task(
            self.writer,
            research_task,
        )

        review_task = create_review_task(
            self.editor,
            writing_task,
        )

        crew = Crew(
            agents=[
                self.researcher,
                self.writer,
                self.editor,
            ],
            tasks=[
                research_task,
                writing_task,
                review_task,
            ],
            process=Process.sequential,
            verbose=True,
        )

        return crew.kickoff(
            inputs={
                "topic": topic,
                "language": language,
                "cover_sheet": cover_sheet or {},
            },
        )
