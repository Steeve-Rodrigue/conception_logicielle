# JobPilot

> Votre application pour la recherche d'emploi.

JobPilot est une application web qui agrège les offres d'emploi issues de l'API France Travail et vous permet de les explorer, les filtrer et de construire votre profil professionnel enrichi de compétences.

---

## Fonctionnalités

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

- Docker et Docker Compose installés
- Un compte [France Travail Entreprise](https://francetravail.io/) pour obtenir les credentials API

---

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/ton-username/jobpilot.git
cd jobpilot
```

### 2. Configurer les variables d'environnement

Copier le fichier template et le remplir avec vos valeurs :

```bash
cp backend/.env.template backend/.env
```

Le fichier `backend/.env.template` contient toutes les variables nécessaires avec leurs descriptions. Les variables obligatoires à renseigner sont :

| Variable | Description |
|---|---|
| `POSTGRES_PASSWORD` | Mot de passe PostgreSQL — choisi librement en local |
| `CLIENT_ID_FRANCE_TRAVAIL` | Client ID de l'API France Travail |
| `CLIENT_SECRET_FRANCE_TRAVAIL` | Secret de l'API France Travail |
| `VITE_API_BASE_URL` | URL du backend (`http://127.0.0.1:8000` en local) |

> Ne jamais commiter le fichier `.env` — il est dans le `.gitignore`.

---

## Déploiement

### Docker Compose (recommandé)

Lance tous les services depuis la racine du projet :

```bash
docker compose --env-file backend/.env up --build
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
