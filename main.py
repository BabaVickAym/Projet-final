from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict
from uuid import uuid4



class Project(BaseModel):
    studentName: str
    course: str
    githubUrl: HttpUrl
    grade: Optional[float] = None


# In-memory store: id -> Project
projects: Dict[str, Project] = {}


@app.post("/projects")
def create_project(project: Project):
    project_id = str(uuid4())
    projects[project_id] = project
    return {"id": project_id, **project.dict()}


@app.get("/projects")
def list_projects():
    return [{"id": pid, **p.dict()} for pid, p in projects.items()]


@app.get("/projects/{id}")
def get_project(id: str):
    if id not in projects:
        raise HTTPException(status_code=404, detail="project not found")
    p = projects[id]
    return {"id": id, **p.dict()}


class Grade(BaseModel):
    grade: float


@app.put("/projects/{id}/grade")
def grade_project(id: str, payload: Grade):
    if id not in projects:
        raise HTTPException(status_code=404, detail="project not found")
    project = projects[id]
    project.grade = payload.grade
    projects[id] = project
    return {"id": id, **project.dict()}


@app.delete("/projects/{id}")
def delete_project(id: str):
    if id not in projects:
        raise HTTPException(status_code=404, detail="project not found")
    del projects[id]
    return {"message": f"project {id} deleted successfully"}


@app.get("/projects/course/{courseName}")
def projects_by_course(courseName: str):
    filtered = [
        {"id": pid, **p.dict()} for pid, p in projects.items() if p.course == courseName
    ]
    return filtered
