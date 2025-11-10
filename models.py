from pydantic import BaseModel, Field
from typing import Optional

class ProjectIn(BaseModel):
    studentName: str
    course: str
    githubUrl: str

class Project(ProjectIn):
    id: str
    grade: Optional[int] = None

class GradeUpdate(BaseModel):
    grade: int = Field(..., ge=0, le=20)
