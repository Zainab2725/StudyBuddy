import os
from crewai import LLM

MODEL_NAME = "openai/gpt-oss-120b"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"


def get_llm():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. "
            "Add it in Streamlit Cloud → Settings → Secrets."
        )

    return LLM(
        model=MODEL_NAME,
        api_key=api_key,
        base_url=GROQ_BASE_URL,
        temperature=1.0,
    )
