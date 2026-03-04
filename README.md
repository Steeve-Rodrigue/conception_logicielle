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

## Configuration des variables d'environnement

Copier le fichier template et le remplir avec vos valeurs, puis le copier à la racine pour Docker Compose :

```bash
cp backend/.env.template backend/.env
cp backend/.env .env
```

Le fichier `backend/.env.template` contient toutes les variables nécessaires avec leurs descriptions. Les variables obligatoires à renseigner sont :

| Variable | Description |
|---|---|
| `POSTGRES_PASSWORD` | Mot de passe PostgreSQL |
| `CLIENT_ID_FRANCE_TRAVAIL` | Client ID de l'API France Travail |
| `CLIENT_SECRET_FRANCE_TRAVAIL` | Secret de l'API France Travail |
| `VITE_API_BASE_URL` | URL du backend (voir section déploiement) |

> Ne jamais commiter le fichier `.env` — il est dans le `.gitignore`.

---

## Déploiement

### Option 1 — Docker Compose (recommandé en local)

Lance tous les services en une seule commande depuis la racine du projet :

```bash
docker compose up --build
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

### Option 2 — Conteneurs individuels

**Backend**

```bash
cd backend
docker build -t backend-app .
docker run -d --name backend-container -p 8000:8000 backend-app
docker ps  # Vérifier que le conteneur tourne
```

**Frontend**

```bash
cd frontend
docker build --build-arg VITE_API_BASE_URL=http://localhost:8000 -t frontend-app .
docker run -d --name frontend-container -p 3000:80 frontend-app
docker ps  # Vérifier que le conteneur tourne
```

> `--build-arg` permet de passer `VITE_API_BASE_URL` au moment du build. Cette valeur est compilée par Vite dans le JS — elle ne peut pas être changée au runtime sans rebuilder l'image.

---

### Option 3 — Kubernetes (SSPCloud)

#### Pusher les images sur Docker Hub

```bash
# Backend
docker build -t votre-username/backend:latest ./backend
docker push votre-username/backend:latest

# Frontend — builder avec l'URL du backend Kubernetes
docker build --build-arg VITE_API_BASE_URL=https://jobpilot-backend.kub.sspcloud.fr -t votre-username/frontend:latest ./frontend
docker push votre-username/frontend:latest
```

> Le frontend nécessite un build dédié par environnement car `VITE_API_BASE_URL` est compilée dans l'image.

#### Configurer les secrets Kubernetes

```bash
cp k8s/secret.yaml.example k8s/secret.yaml
```

Renseigner les credentials dans `k8s/secret.yaml` — ce fichier ne doit jamais être commité.

Pour récupérer les credentials PostgreSQL du cluster SSPCloud :

```bash
kubectl get secret postgresql-cnpg-XXXXXX-app -o jsonpath='{.data.user}' | base64 --decode
kubectl get secret postgresql-cnpg-XXXXXX-app -o jsonpath='{.data.password}' | base64 --decode
kubectl get secret postgresql-cnpg-XXXXXX-app -o jsonpath='{.data.dbname}' | base64 --decode
kubectl get secret postgresql-cnpg-XXXXXX-app -o jsonpath='{.data.host}' | base64 --decode
```

#### Déployer sur le cluster

```bash
kubectl apply -f k8s/
```

#### Vérifier le déploiement

```bash
kubectl get pods -w
```

| Service | URL |
|---|---|
| Frontend | https://jobpilot.kub.sspcloud.fr |
| Backend API | https://jobpilot-backend.kub.sspcloud.fr |
| Documentation Swagger | https://jobpilot-backend.kub.sspcloud.fr/docs |

---

## Application en ligne

L'application est déployée et accessible directement sans installation :

| Service | URL |
|---|---|
| Application | https://jobpilot.kub.sspcloud.fr |
| API | https://jobpilot-backend.kub.sspcloud.fr |
| Documentation API | https://jobpilot-backend.kub.sspcloud.fr/docs |

---
