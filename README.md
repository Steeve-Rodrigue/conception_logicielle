# JobPilot

> Votre application pour la recherche d'emploi.

JobPilot est une application web qui agrège les offres d'emploi issues de l'API France Travail et vous permet de les explorer, les filtrer et de construire votre profil professionnel enrichi de compétences.

---

## Fonctionnalités

- **Récupération des offres** — Les offres sont automatiquement récupérées et stockées depuis France Travail au démarrage de l'application
- **Recherche d'offres d'emploi** — Accédez aux offres data/IA en temps réel via l'API France Travail
- **Authentification** — Créez un compte et connectez-vous de façon sécurisée
- **Filtres de recherche** — Affinez les offres par métier, localisation, type de contrat
- **Profil utilisateur** — Construisez votre profil et ajoutez vos compétences

---

## Application en ligne

L'application est déployée et accessible directement sans installation :

| Service | URL |
|---|---|
| Application | https://jobpilot.kub.sspcloud.fr |
| API | https://jobpilot-backend.kub.sspcloud.fr |
| Documentation API | https://jobpilot-backend.kub.sspcloud.fr/docs |

---

## Stack technique

| Composant | Technologie |
|---|---|
| Backend | FastAPI + Python 3.13 |
| Frontend | React + Vite + TailwindCSS |
| Base de données | PostgreSQL 14 |
| Conteneurisation | Docker + Docker Compose |
| Orchestration | Kubernetes (SSPCloud) |
| API externe | France Travail |

---

## Prérequis

- Docker installés
- Un compte [France Travail Entreprise](https://francetravail.io/) pour obtenir les credentials API

---

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/isaolivia2001/Projet-Conception-logicielle.git
cd Projet-Conception-logicielle
```

### 2. Configurer les variables d'environnement
Se situer a la racine : 
Copier les fichiers env.template(situé a la racine du projet, dans le dossier backend et dans le dossier Frontend) et les remplir avec vos valeurs ;Certaines valeures sont par defaut.

```bash
# Copier le template du backend
cp backend/.env.template backend/.env

# Copier le template de la racine
cp .env.template .env

# Copier le template du frontend
cp frontend/.env.template frontend/.env
```

Le fichier `backend/.env.template` contient toutes les variables nécessaires avec leurs descriptions. 
Les variables obligatoires à renseigner Pour le lancement local avec Docker est :

| Variable | Description |
|---|---|
| `CLIENT_ID_FRANCE_TRAVAIL` | Client ID de l'API France Travail |
| `CLIENT_SECRET_FRANCE_TRAVAIL` | Secret de l'API France Travail |

---

## Déploiement

### Docker Compose (recommandé)

Lance tous les services depuis la racine du projet :

```bash
sudo docker compose  up --build
```

L'application démarre dans cet ordre :

```
PostgreSQL (healthy)
    ↓
init-db (initialisation de la base)
    ↓
Backend (running)
    ↓
Frontend (running)
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Documentation Swagger | http://localhost:8000/docs |

Pour arrêter :

```bash
docker compose down        # conserve les données PostgreSQL
docker compose down -v     # supprime aussi le volume PostgreSQL
```

---





### Lancement sans Docker

**Prérequis**

- Python 3.13+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Node.js 20+
- Une instance PostgreSQL locale

**Backend**
```bash
cd backend

# Installer les dépendances
uv sync

# Lancer le serveur
uv run python src/api.py
```

**Frontend**
```bash
cd frontend

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

**Base de données**

Adapter les variables suivantes dans `backend/.env` en fonction de ton installation PostgreSQL :
```env
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_USER=
POSTGRES_PASSWORD=        
POSTGRES_DATABASE=
```

Puis initialiser la base :
```bash
cd backend
uv run python src/dao/reset_database.py
```
**Variables obligatoires**

Se référer au fichier `backend/.env.template` pour la liste complète. Les variables obligatoires sont :

| Variable | Description |
|---|---|
| `POSTGRES_HOST` | Hôte PostgreSQL (`localhost` par défaut) |
| `POSTGRES_PORT` | Port PostgreSQL (`5432` par défaut) |
| `POSTGRES_USER` | Utilisateur PostgreSQL |
| `POSTGRES_PASSWORD` | Mot de passe PostgreSQL |
| `POSTGRES_DATABASE` | Nom de la base de données |
| `POSTGRES_SCHEMA` | Schéma PostgreSQL (`app` — ne pas modifier) |
| `CLIENT_ID_FRANCE_TRAVAIL` | Client ID de l'API France Travail |
| `CLIENT_SECRET_FRANCE_TRAVAIL` | Secret de l'API France Travail |

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://127.0.0.1:8000 |
| Documentation Swagger | http://127.0.0.1:8000/docs |
