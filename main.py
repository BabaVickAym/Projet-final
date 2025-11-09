from fastapi import FastAPI, HTTPException
from data_manager import load_data, save_data
from models import Project, ProjectIn, GradeUpdate
from typing import List
import uuid
# import flask
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ProjetAPI - Gestion des Soumissions")


# --- Début de la correction CORS ---
origins = [
    "*",  # Autorise toutes les origines pour le développement
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- Fin de la correction CORS ---

# Chargement initial des données
data = load_data()


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur ProjetAPI"}


# Endpoint 1: POST /projects (Soumettre un nouveau projet)
@app.post("/projects", response_model=Project, status_code=201)
def create_project(project_in: ProjectIn):
    # Générer un ID unique
    new_id = str(uuid.uuid4())
    # Créer l'objet Project complet
    new_project = Project(id=new_id, **project_in.model_dump())

    # Ajouter à la liste et sauvegarder
    data["projects"].append(new_project.model_dump())
    save_data(data)

    return new_project


# Endpoint 2: GET /projects (Lister tous les projets)
@app.get("/projects", response_model=List[Project])
def list_projects():
    # Retourne la liste des projets
    return data["projects"]


# Endpoint 3: GET /projects/{id} (Obtenir les détails d'un projet spécifique)
@app.get("/projects/{project_id}", response_model=Project)
def get_project(project_id: str):
    # Chercher le projet dans la liste
    project_data = next((p for p in data["projects"] if p["id"] == project_id), None)

    if project_data is None:
        raise HTTPException(status_code=404, detail="Projet non trouvé")

    # Retourner le projet trouvé
    return project_data


# Endpoint 4: PUT /projects/{id}/grade (Permettre à un "professeur" de noter un projet)
@app.put("/projects/{project_id}/grade", response_model=Project)
def grade_project(project_id: str, grade_update: GradeUpdate):
    # Trouver l'index du projet
    project_index = next(
        (i for i, p in enumerate(data["projects"]) if p["id"] == project_id), -1
    )

    if project_index == -1:
        raise HTTPException(status_code=404, detail="Projet non trouvé")

    # Mettre à jour la note
    data["projects"][project_index]["grade"] = grade_update.grade

    # Sauvegarder les données
    save_data(data)

    # Retourner le projet mis à jour
    return data["projects"][project_index]


# Endpoint 5: DELETE /projects/{id} (Supprimer une soumission de projet)
@app.delete("/projects/{project_id}", status_code=204)
def delete_project(project_id: str):
    global data  # Nécessaire pour modifier la variable globale 'data'

    # Trouver l'index du projet
    project_index = next(
        (i for i, p in enumerate(data["projects"]) if p["id"] == project_id), -1
    )

    if project_index == -1:
        raise HTTPException(status_code=404, detail="Projet non trouvé")

    # Supprimer le projet de la liste
    del data["projects"][project_index]

    # Sauvegarder les données
    save_data(data)

    # Retourne un statut 204 No Content
    return


# Endpoint 6: GET /projects/course/{courseName} (Filtrer les projets par cours)
@app.get("/projects/course/{course_name}", response_model=List[Project])
def get_projects_by_course(course_name: str):
    # Filtrer les projets dont le nom de cours correspond (insensible à la casse)
    filtered_projects = [
        p for p in data["projects"] if p["course"].lower() == course_name.lower()
    ]

    if not filtered_projects:
        # Le TP ne spécifie pas de 404, nous retournons une liste vide pour rester simple.
        pass

    return filtered_projects
