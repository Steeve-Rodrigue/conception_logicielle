# Projet-Conception-logicielle

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
