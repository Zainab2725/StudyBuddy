from crewai import Agent
from config import get_llm

def create_quiz_agent(document_tool, memory_tool):
    return Agent(
        role="Quiz Master",
        goal="Create useful questions that test understanding and application.",
        backstory="You are an educational assessment specialist. Build questions from the uploaded material and avoid shallow memorization.",
        llm=get_llm(), tools=[document_tool, memory_tool], verbose=True, allow_delegation=False
    )
