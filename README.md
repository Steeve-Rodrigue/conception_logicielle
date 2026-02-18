# Configuration de l'application JOBPILOT

Ce document explique la configuration de l'application à l'aide du fichier `.env`.



1. Copiez le fichier template dans le dossier backend pour créer le fichier `.env` :
   ```bash
   cd backend
   cp .env.template .env
   ```
2. Remplissez vos valeurs réelles pour PostgreSQL, les identifiants France Travail, etc.



## 1. Base de données
### PostgreSQL 

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mot_de_passe
POSTGRES_DATABASE=nom_de_la_base
POSTGRES_SCHEMA=app
```


> `POSTGRES_SCHEMA` doit rester `app` (obligatoire pour l'application).



## 2. Frontend (VITE)

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
FRONTEND_URL=http://localhost:5173
```

- `VITE_API_BASE_URL` → URL de base de l'API backend que le frontend utilisera.
- `FRONTEND_URL` → URL où le frontend est exécuté.

> **Important :** Les variables commençant par `VITE_` sont exposées au frontend. Les autres restent côté backend.  



## 3. CORS (Cross-Origin Resource Sharing)

```env
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:5173", "http://localhost:8000"]
```

- Liste des origines autorisées à accéder à l'API backend.
- Assurez-vous que l'URL de votre frontend y figure pour éviter les erreurs CORS.



## 4. API externe – France Travail (Pôle Emploi)

```env
CLIENT_ID_FRANCE_TRAVAIL=votre_client_id_ici
CLIENT_SECRET_FRANCE_TRAVAIL=votre_client_secret_ici
```

- Ces identifiants sont nécessaires pour accéder à l'API France Travail.
- Obtenez-les sur [https://francetravail.io](https://francetravail.io).











## Backend API
### Premières commandes
```bash
# Se placer dans le dossier backtend
cd backend

# Installer les dépendances
uv sync

# Lancer le serveur de développement
uv run uvicorn src.api:app --reload 
```



## Frontend

### Premières commandes
```bash
# Se placer dans le dossier frontend
cd frontend

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```




## Backend - Linting et formatage (Ruff) (Pour developeur)

### Installation de pre-commit
```bash
# Se placer dans le dossier backend
cd backend

# Ajouter pre-commit comme dépendance de développement
uv add --dev pre-commit

# Installer les hooks Git
uv run pre-commit install
```

### Utilisation de pre-commit
```bash
# Vérifier un dossier spécifique
uv run pre-commit run --files <nom_du_dossier>

# Exemples :
# Tous les fichiers de src
uv run pre-commit run --files src/*

# Tous les fichiers du projet
uv run pre-commit run --all-files
```
