from fastapi import FastAPI
import json
from pathlib import Path

app = FastAPI(
    title="ProjetAPI- Gestion des projets étudiants",
    description="API pour soumettre, consulter et noter des projets étudiants.",
    version="1.0.0",
)

DB_PATH = Path("db.json")


@app.get(
    "/projects",
    summary="Lister tous les projets",
    tags=["Projets"],
)
def get_projects():
    """
    Retourne la liste de tous les projets soumis.
    Les données sont lues depuis le fichier `db.json`
    """
    try:
        with open(DB_PATH, "r", encoding="utf-8") as db:
            projects = json.load(db)
        return projects
    except Exception as e:
        return {"error": "Impossible de lire les projets", "details": str(e)}
