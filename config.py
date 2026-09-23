import os
from crewai import LLM

MODEL_NAME = "groq/openai/gpt-oss-120b"


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
        temperature=0.2,
        provider="groq",
    )
