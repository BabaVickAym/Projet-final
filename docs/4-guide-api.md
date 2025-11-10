# Guide des Endpoints de l'API

Voici la liste de tous les endpoints disponibles et comment les utiliser.

---

### 1. `POST /projects`

Soumet un nouveau projet.

-   **Méthode :** `POST`
-   **Endpoint :** `/projects`
-   **Corps de la requête (Body ) :** `JSON`
    ```json
    {
      "studentName": "Marie Curie",
      "course": "Physique Nucléaire",
      "githubUrl": "https://github.com/marie/radium-project"
    }
    ```
-   **Réponse (Succès ) :** `201 Created`
    ```json
    {
      "id": "un-id-unique-genere",
      "studentName": "Marie Curie",
      "course": "Physique Nucléaire",
      "githubUrl": "https://github.com/marie/radium-project",
      "grade": null
    }
    ```

---

### 2. `GET /projects`

Liste tous les projets soumis.

-   **Méthode :** `GET`
-   **Endpoint :** `/projects`
-   **Réponse (Succès ) :** `200 OK`
    ```json
    [
      {
        "id": "un-id-unique-genere",
        "studentName": "Marie Curie",
        "course": "Physique Nucléaire",
        "githubUrl": "https://github.com/marie/radium-project",
        "grade": null
      }
    ]
    ```

---

### 3. `GET /projects/:id`

Obtient les détails d'un projet spécifique.

-   **Méthode :** `GET`
-   **Endpoint :** `/projects/un-id-unique-genere`
-   **Réponse (Succès ) :** `200 OK`
    ```json
    {
      "id": "un-id-unique-genere",
      "studentName": "Marie Curie",
      "course": "Physique Nucléaire",
      "githubUrl": "https://github.com/marie/radium-project",
      "grade": null
    }
    ```

---

### 4. `PUT /projects/:id/grade`

Permet de noter un projet.

-   **Méthode :** `PUT`
-   **Endpoint :** `/projects/un-id-unique-genere/grade`
-   **Corps de la requête (Body ) :** `JSON`
    ```json
    {
      "grade": 18
    }
    ```
-   **Réponse (Succès) :** `200 OK`
    ```json
    {
      "id": "un-id-unique-genere",
      "studentName": "Marie Curie",
      "course": "Physique Nucléaire",
      "githubUrl": "https://github.com/marie/radium-project",
      "grade": 18
    }
    ```

---

### 5. `DELETE /projects/:id`

Supprime une soumission de projet.

-   **Méthode :** `DELETE`
-   **Endpoint :** `/projects/un-id-unique-genere`
-   **Réponse (Succès ) :** `204 No Content` (Pas de contenu dans la réponse)

---

### 6. `GET /projects/course/:courseName`

Filtre et retourne tous les projets d'un cours spécifique.

-   **Méthode :** `GET`
-   **Endpoint :** `/projects/course/Physique%20Nucl%C3%A9aire`
-   **Réponse (Succès) :** `200 OK`
    ```json
    [
      {
        "id": "un-id-unique-genere",
        "studentName": "Marie Curie",
        "course": "Physique Nucléaire",
        "githubUrl": "https://github.com/marie/radium-project",
        "grade": 18
      }
    ]
    ```
