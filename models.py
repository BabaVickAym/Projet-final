from pydantic import BaseModel, HttpUrl
from typing import Optional

class ProjectCreate(BaseModel):
    studentName: str
    course: str
    githubUrl: Optional[HttpUrl] = None

class ProjectUpdate(BaseModel):
    studentName: Optional[str] = None
    course: Optional[str] = None
    githubUrl: Optional[HttpUrl] = None

class GradeUpdate(BaseModel):
    grade: int

class ProjectResponse(ProjectCreate):
    id: int
    grade: Optional[int] = None
