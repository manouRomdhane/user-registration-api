# CSV Blank — Spring Boot + Angular

Création d'un fichier **CSV vide** (blanc) dont le nom est la date du jour + heure + minute.

Exemple de nom : `2026-07-27_14-35.csv`

## Backend (Spring Boot)

```bash
cd backend
mvn spring-boot:run
```

API : `POST http://localhost:8080/api/csv/create`

Les fichiers sont écrits dans `backend/exports/`.

## Frontend (Angular)

```bash
cd frontend
npm install
npm start
```

Ouvrir http://localhost:4200 et cliquer sur **Créer un CSV vide**.
