import os
import sys
from google import genai

# Le diff est passé en argument au script
# Le contenu du diff est encodé pour éviter les problèmes de shell
diff_content = sys.argv[1].replace("%0A", "\n").replace("%0D", "\r").replace("%25", "%")

# Le prompt pour le LLM
PROMPT = f"""
Tu es un relecteur de code expert. Analyse le 'diff' de code suivant.
Si le code est bon, fournis des pistes d'amélioration.
Si le code contient des bugs ou des problèmes de sécurité, liste-les.
Réponds en français.

--- DIFF DE CODE ---
{diff_content}
"""

# Récupérer la clé d'API depuis les variables d'environnement (GitHub Secret)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    # Ceci ne devrait pas arriver si le secret est bien configuré dans le workflow
    print("Erreur: La clé GEMINI_API_KEY n'est pas configurée.")
    sys.exit(1)

try:
    # Initialisation du client Gemini
    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=PROMPT,
    )

    # Afficher la réponse du LLM (sera capturée par le workflow)
    # Nous ajoutons un titre pour le commentaire GitHub
    print("**Revue de Code par l'IA (Gemini)**\n")
    print(response.text)

except Exception as e:
    print(f"Erreur lors de l'appel à l'API Gemini: {e}")
    sys.exit(1)
