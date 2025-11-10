from fastapi import APIRouter
from data_manager import load_data
from models import Project
from typing import List

router = APIRouter()

@router.get("/projects/course/{course_name}", response_model=List[Project])
def get_projects_by_course(course_name: str):
    data = load_data()
    filtered_projects = [
        p for p in data["projects"] if p["course"].lower() == course_name.lower()
    ]
    return filtered_projects
