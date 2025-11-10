from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from uuid import uuid4

app = FastAPI()


class project(BaseModel):
    studentName: str
    course: str
    githubUrl: str
    grade: Optional[float] = None

    projects = {}

    @app.post("/projects")
    def create_project(project: projects):
        project_id = str(uuid4())
        project[uuid4] = project.dict()
        return {"id": project_id, **project.dict()}

    @app.delete("/projects/{id}")
    def delete_project(id: str):
        if id not in project:
            raise HTTPException(status_code=404, detail="project not found")

        del project[id]
        return {"message": f"project {id} delete successfully"}
