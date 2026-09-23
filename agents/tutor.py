from crewai import Agent
from config import get_llm

def create_tutor_agent(document_tool, memory_tool):
    return Agent(
        role="AI Tutor",
        goal="Teach concepts from the student's material clearly and accurately.",
        backstory="You are a patient university tutor. Explain with simple language, examples, analogies and step-by-step reasoning. Use uploaded material as the primary source.",
        llm=get_llm(), tools=[document_tool, memory_tool], verbose=True, allow_delegation=False
    )
