from crewai import Crew, Process, Task
from agents.tutor import create_tutor_agent

def create_tutor_crew(document_tool, memory_tool, question):
    tutor = create_tutor_agent(document_tool, memory_tool)
    task = Task(
        description=f"""The student asks: {question}

Answer the question using the uploaded study material as the primary source. Explain simply, give an example where useful, and say when the material does not contain enough information. Do not invent facts.""",
        expected_output="A clear, accurate tutor response.",
        agent=tutor
    )
    return Crew(agents=[tutor], tasks=[task], process=Process.sequential, verbose=True)
