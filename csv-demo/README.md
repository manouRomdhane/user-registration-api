# CSV Demo — Spring Boot + Angular

Exemple minimal : un bouton Angular crée / télécharge un **fichier CSV vide** via une API Spring Boot.

## Structure

```text
csv-demo/
├── backend/     # Spring Boot (port 8080)
└── frontend/    # Angular (port 4200)
```

## API Spring Boot

| Méthode | URL | Description |
|---------|-----|-------------|
| `GET` | `/api/csv/empty?fileName=empty.csv` | Télécharge un CSV vide |
| `POST` | `/api/csv/empty?fileName=empty.csv` | Crée un CSV vide sur le serveur (`./exports`) |

### Lancer le backend

```bash
cd csv-demo/backend
./mvnw spring-boot:run
```

Test rapide :

```bash
curl -OJ "http://localhost:8080/api/csv/empty?fileName=test.csv"
curl -X POST "http://localhost:8080/api/csv/empty?fileName=serveur.csv"
```

## Frontend Angular

### Lancer le frontend

```bash
cd csv-demo/frontend
npm install
npm start
```

Ouvrir http://localhost:4200

- **Télécharger un CSV vide** → appelle `GET /api/csv/empty` et déclenche le download navigateur
- **Créer sur le serveur** → appelle `POST /api/csv/empty` et affiche le nom du fichier créé

## Points clés du code

**Backend** (`CsvController.java`) :
- renvoie un corps vide avec `Content-Disposition: attachment`
- ou écrit un fichier `.csv` vide dans le dossier configurable `csv.export-dir`

**Frontend** (`csv.service.ts` + bouton dans `app.component`) :
- `HttpClient` + `responseType: 'blob'` pour le téléchargement
- création d’un lien `<a download>` pour sauver le fichier côté client
