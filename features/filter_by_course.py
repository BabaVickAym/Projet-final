import json
from fastapi import FastAPI, HTTPException

app = FastAPI()

DB_FILE = "db_test.json"  # fichier local de test

def load_projects():
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f).get("projects", [])

@app.get("/projects/course/{course_name}")
def get_projects_by_course(course_name: str):
    projects = load_projects()
    filtered = [p for p in projects if p.get("course", "").lower() == course_name.lower()]

    if not filtered:
        raise HTTPException(status_code=404, detail="Aucun projet trouvé pour ce cours")

    return {"course": course_name, "projects": filtered}
