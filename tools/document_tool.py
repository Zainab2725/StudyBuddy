from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class DocumentSearchInput(BaseModel):
    query: str = Field(..., description="Topic or question to search for.")

class StudyMaterialTool(BaseTool):
    name: str = "Study Material Search"
    description: str = "Searches the student's uploaded study material for relevant information."
    args_schema: Type[BaseModel] = DocumentSearchInput
    material: str = ""

    def _run(self, query: str) -> str:
        if not self.material:
            return "No study material has been uploaded."
        words = [w.lower() for w in query.split() if len(w) > 2]
        results = []
        for paragraph in self.material.splitlines():
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            score = sum(1 for word in words if word in paragraph.lower())
            if score:
                results.append((score, paragraph))
        results.sort(key=lambda x: x[0], reverse=True)
        return "\n\n".join(p for _, p in results[:8]) or "No directly matching section was found."
