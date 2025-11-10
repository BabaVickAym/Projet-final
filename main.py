from fastapi import FastAPI, HTTPException
from typing import List
from uuid import uuid4
from models import ProjectCreate, ProjectUpdate, ProjectResponse, GradeUpdate
from data_manager import load_data, save_data
from features.filter_by_course import router as filter_router

app = FastAPI(
    title="Projet Final FastAPI",
    description="API de gestion de projets étudiants avec filtrage, notation et CRUD complet.",
    version="2.0.0"
)

# Inclure les routes modularisées
app.include_router(filter_router)


# ✅ Lister tous les projets
@app.get("/projects", response_model=List[ProjectResponse])
def get_projects():
    data = load_data()
    return data.get("projects", [])


# ✅ Récupérer un projet par ID
@app.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str):
    data = load_data()
    for project in data.get("projects", []):
        if project["id"] == project_id:
            return project
    raise HTTPException(status_code=404, detail="Projet non trouvé")


# ✅ Créer un nouveau projet
@app.post("/projects", response_model=ProjectResponse, status_code=201)
def create_project(project: ProjectCreate):
    data = load_data()
    projects = data.get("projects", [])

    # Génération d'un ID unique (UUID)
    new_id = str(uuid4())

    new_project = {
        "id": new_id,
        "studentName": project.studentName,
        "course": project.course,
        "githubUrl": project.githubUrl,
        "grade": None
    }

    projects.append(new_project)
    data["projects"] = projects
    save_data(data)

    return new_project


# ✅ Mettre à jour un projet existant
@app.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: str, updated_data: ProjectUpdate):
    data = load_data()
    for project in data.get("projects", []):
        if project["id"] == project_id:
            if updated_data.studentName is not None:
                project["studentName"] = updated_data.studentName
            if updated_data.course is not None:
                project["course"] = updated_data.course
            if updated_data.githubUrl is not None:
                project["githubUrl"] = updated_data.githubUrl

            save_data(data)
            return project
    raise HTTPException(status_code=404, detail="Projet non trouvé")


# ✅ Supprimer un projet
@app.delete("/projects/{project_id}", status_code=204)
def delete_project(project_id: str):
    data = load_data()
    projects = data.get("projects", [])
    new_projects = [p for p in projects if p["id"] != project_id]

    if len(new_projects) == len(projects):
        raise HTTPException(status_code=404, detail="Projet non trouvé")

    data["projects"] = new_projects
    save_data(data)
    return {"message": "Projet supprimé avec succès"}


# ✅ Noter un projet
@app.put("/projects/{project_id}/grade", response_model=ProjectResponse)
def grade_project(project_id: str, grade_data: GradeUpdate):
    data = load_data()
    for project in data.get("projects", []):
        if project["id"] == project_id:
            project["grade"] = grade_data.grade
            save_data(data)
            return project
    raise HTTPException(status_code=404, detail="Projet non trouvé")
