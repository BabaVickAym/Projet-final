# features/filter_by_course.py
from fastapi import APIRouter
from typing import List
from models import ProjectResponse  # On utilise le modèle existant dans models.py
from data_manager import load_data  # Je suppose que tu as un fichier data_manager.py qui charge les projets

router = APIRouter()

@router.get("/projects/course/{course_name}", response_model=List[ProjectResponse])
def get_projects_by_course(course_name: str):
    """
    Renvoie la liste des projets filtrés par nom de cours.
    """
    data = load_data()  # Charge tes données depuis data_manager
    filtered_projects = [
        ProjectResponse(**p) for p in data["projects"]
        if p["course"].lower() == course_name.lower()
    ]
    return filtered_projects
