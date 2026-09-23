from crewai import Crew, Process, Task
from agents.planner import create_planner_agent
from agents.tutor import create_tutor_agent
from agents.quiz import create_quiz_agent
from agents.analyzer import create_analyzer_agent

def create_study_crew(document_tool, memory_tool):
    planner = create_planner_agent(document_tool, memory_tool)
    tutor = create_tutor_agent(document_tool, memory_tool)
    quiz = create_quiz_agent(document_tool, memory_tool)
    analyzer = create_analyzer_agent(memory_tool)

    planning = Task(
        description="""Analyze the uploaded study material. Determine the main subject, learning objectives, important concepts and subtopics, difficulty, prerequisites, and recommended study order. Do not simply summarize. Answer: What exactly does the student need to study?""",
        expected_output="A structured study roadmap with subject, objectives, concepts, subtopics, difficulty, prerequisites and study order.",
        agent=planner
    )
    teaching = Task(
        description="""Using the roadmap, prepare beginner-friendly teaching notes for the most important concepts. For each concept include a simple definition, explanation, example and common misunderstanding.""",
        expected_output="Structured teaching notes for the major concepts.",
        agent=tutor, context=[planning]
    )
    quiz_task = Task(
        description="""Create five practice questions based on the roadmap and teaching notes. Mix conceptual, application and understanding questions. Include answers and explanations.""",
        expected_output="Five practice questions with answers and explanations.",
        agent=quiz, context=[planning, teaching]
    )
    audit = Task(
        description="""Create a learning-audit framework explaining how quiz results can reveal strong topics, weak topics, knowledge gaps and the next recommended study action.""",
        expected_output="A structured learning audit framework.",
        agent=analyzer, context=[planning, quiz_task]
    )
    return Crew(
        agents=[planner, tutor, quiz, analyzer],
        tasks=[planning, teaching, quiz_task, audit],
        process=Process.sequential,
        verbose=True
    )
