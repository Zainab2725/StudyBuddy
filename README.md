# StudyBuddy

StudyBuddy is a multi-agent learning workspace that turns uploaded study material into a focused study experience.

## Core flow

Learning Material → Understand → Structure → Teach → Test → Audit

## Features

- PDF study-material upload
- AI study planning
- Structured study pack
- AI tutor
- Practice quiz generation
- Learning audit
- Student memory tool
- Study-material search tool
- CrewAI multi-agent architecture
- Groq GPT-OSS 120B

## Deploy

1. Upload this project to GitHub.
2. Create a new Web Service on Render.
3. Connect the GitHub repository.
4. Build command: `pip install -r requirements.txt`
5. Start command: `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT`
6. Add `GROQ_API_KEY` as an environment variable.

Do not commit your API key.
