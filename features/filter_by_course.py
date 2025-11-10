# features/filter_by_course.py
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException

# Crée un routeur FastAPI (pas app = FastAPI() ici)
router = APIRouter()

# Chemin vers le fichier db.json
DB_FILE = Path(__file__).parent / "db.json"

def load_projects():
    if not DB_FILE.exists():
        return []  # retourne une liste vide si db.json n'existe pas
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f).get("projects", [])

@router.get("/projects/course/{course_name}")
def get_projects_by_course(course_name: str):
    projects = load_projects()
    filtered = [p for p in projects if p.get("course", "").lower() == course_name.lower()]

    if not filtered:
        raise HTTPException(status_code=404, detail="Aucun projet trouvé pour ce cours")

    return {"course": course_name, "projects": filtered}
