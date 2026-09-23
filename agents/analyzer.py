from crewai import Agent
from config import get_llm

def create_analyzer_agent(memory_tool):
    return Agent(
        role="Learning Analyst",
        goal="Identify learning gaps and recommend the next study action.",
        backstory="You analyze student performance, study history and weak topics to guide the next learning step.",
        llm=get_llm(), tools=[memory_tool], verbose=True, allow_delegation=False
    )
