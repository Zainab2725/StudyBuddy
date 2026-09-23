import json
import os
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

MEMORY_FILE = "studybuddy_memory.json"

class MemoryInput(BaseModel):
    action: str = Field(..., description="Use 'remember: information' or 'recall'.")

class StudentMemoryTool(BaseTool):
    name: str = "Student Memory"
    description: str = "Stores and retrieves important student learning information."
    args_schema: Type[BaseModel] = MemoryInput

    def _load(self):
        if not os.path.exists(MEMORY_FILE):
            return []
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _run(self, action: str):
        memories = self._load()
        action = action.strip()
        if action.lower() == "recall":
            return "\n".join(f"- {x}" for x in memories[-20:]) or "No student memories have been saved yet."
        if action.lower().startswith("remember:"):
            info = action[9:].strip()
            if not info:
                return "No information was provided."
            memories.append(info)
            with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump(memories, f, indent=2, ensure_ascii=False)
            return "Student memory saved successfully."
        return "Invalid action. Use 'remember: information' or 'recall'."
