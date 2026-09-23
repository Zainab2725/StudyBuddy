from crewai import Agent
from config import get_llm

def create_planner_agent(document_tool, memory_tool):
    return Agent(
        role="Study Planner",
        goal="Determine what the student actually needs to study from the uploaded material.",
        backstory="You are an educational planner. Identify important concepts, relationships, difficulty, objectives and study order rather than producing a generic summary.",
        llm=get_llm(), tools=[document_tool, memory_tool], verbose=True, allow_delegation=False
    )
