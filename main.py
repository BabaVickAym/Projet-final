# main.py
from fastapi import FastAPI, HTTPException
from data_manager import load_data, save_data
from models import Project, ProjectIn, GradeUpdate
from typing import List
from fastapi.responses import HTMLResponse
from fastapi import Request
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
@app.post(
    "/projects",
    response_model=Project,
    status_code=201,
    summary="Cette description est intentionnellement très longue pour provoquer une erreur de linting et tester la CI, elle devrait dépasser la limite de 88 caractères",
)
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


# Endpoint 3: GET /projects/{project_id} (Obtenir les détails d'un projet spécifique)
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


# Gestionnaire personnalisé pour les erreurs 404
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Erreur 404 - Projet non trouvé</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #f4f4f4 0%, #e0e0e0 100%);
                color: #333;
                text-align: center;
                padding: 50px;
                margin: 0;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }
            h1 {
                font-size: 80px;
                color: #ff6347;
                margin: 0;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
                animation: bounce 1s ease-in-out infinite;
            }
            p {
                font-size: 20px;
                max-width: 600px;
                margin: 20px auto;
            }
            .button {
                display: inline-block;
                padding: 12px 24px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-weight: 600;
                transition: background-color 0.3s ease;
            }
            .button:hover {
                background-color: #0056b3;
            }
            img {
                max-width: 400px;
                margin: 20px 0;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
        </style>
    </head>
    <body>
        <h1>404</h1>
        <p>Oups ! Le projet que vous cherchez n'existe pas ou a été supprimé. Peut-être a-t-il pris des vacances inattendues ?</p>
        <img src="https://deerdesigner.com/wp-content/uploads/2024/07/Article-59-creative-404-pages_Title-card-opt-4.png.webp" alt="Illustration 404 créative">
        <a href="/" class="button">Retourner à l'accueil</a>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=404)
