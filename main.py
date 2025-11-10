# main.py
from fastapi import FastAPI
from features.filter_by_course import router as course_router

app = FastAPI(title="ProjetAPI", description="API pour la gestion des projets étudiants.")

# Inclusion du routeur
app.include_router(course_router)

# Optionnel : un endpoint racine simple
@app.get("/")
async def read_root():
    return {"message": "Bienvenue sur ProjetAPI"}
