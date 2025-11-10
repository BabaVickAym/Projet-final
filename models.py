from pydantic import BaseModel
from typing import Optional

class ProjectRead(BaseModel):
    studentName: str
    course: str
    githubUrl: Optional[str] = None
