import json
from typing import List, Dict, Any

# from models import Project  # Nous allons utiliser le modèle Project

DB_FILE = "db.json"


def load_data() -> Dict[str, List[Dict[str, Any]]]:
    """Charge les données depuis db.json."""
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Si le fichier n'existe pas, retourne une structure vide
        return {"projects": []}
    except json.JSONDecodeError:
        # Gère le cas où le fichier est vide ou mal formé
        return {"projects": []}


def save_data(data: Dict[str, List[Dict[str, Any]]]):
    """Sauvegarde les données dans db.json."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# Initialisation du fichier si nécessaire
if not load_data().get("projects"):
    save_data({"projects": []})
