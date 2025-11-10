from pydantic import BaseModel, Field
from typing import Optional


# Modèle pour la soumission initiale d'un projet (POST)
class ProjectIn(BaseModel):
    studentName: str = Field(..., description="Nom de l'étudiant ou du groupe.")
    course: str = Field(..., description="Nom du cours auquel le projet est soumis.")
    githubUrl: str = Field(..., description="URL du dépôt GitHub du projet.")


# Modèle pour un projet stocké (inclut l'ID et la note)
class Project(ProjectIn):
    id: str = Field(..., description="Identifiant unique du projet.")
    grade: Optional[int] = Field(None, description="Note attribuée au projet (0-20).")


# Modèle pour la notation (PUT /projects/{id}/grade)
class GradeUpdate(BaseModel):
    grade: int = Field(
        ..., ge=0, le=20, description="Note à attribuer (entre 0 et 20)."
    )
    comment: Optional[str] = Field(
        None,
        max_length=255,
        description="Commentaire facultatif de l'évaluateur concernant le projet."
    )

    class Config:
        schema_extra = {
            "example": {
                "grade": 17,
                "comment": "Très bon projet, bien structuré et documenté."
            }
        }