from typing import Optional
from pydantic import BaseModel, Field

class SingleTodo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="Must be between 1 and 5")
    completed: bool
