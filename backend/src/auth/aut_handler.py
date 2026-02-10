"""
Gestion des tokens JWT et authentification.

Ce fichier contient toutes les fonctions pour :
- Créer un token JWT quand quelqu'un se connecte
- Vérifier un token JWT
- Vérifier un login/mot de passe
- Extraire les infos d'un token
"""

import os
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from dotenv import load_dotenv

from services.user_service import UserService
from utils.security import verify_password


load_dotenv()


JWT_SECRET = os.getenv("JWT_SECRET", "votre_secret_par_defaut")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", "3600"))

user_service = UserService()


def sign_jwt(id_utilisateur: int) -> dict:
    """
    Crée un token JWT pour un utilisateur.

    Appelée après une connexion réussie pour générer le token.

    Parameters
    ----------
    id_utilisateur : int
        ID de l'utilisateur connecté

    Returns
    -------
    dict
        {
            "access_token": "eyJ0eXAiOiJKV1...",
            "token_type": "bearer"
        }
    """
    
    payload = {
        "id_utilisateur": id_utilisateur,
        "exp": datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS),
    }

    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}


def decode_jwt(token: str) -> Optional[dict]:
    """
    Décode un token JWT et vérifie qu'il n'est pas expiré.

    Parameters
    ----------
    token : str
        Le token JWT à décoder

    Returns
    -------
    dict or None
        Les données du token si valide, None sinon

    Example
    -------
    decoded = decode_jwt(token)
    # {"id_utilisateur": 1, "exp": 1234567890}
    """
    try:
       
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

       
        if (
            decoded.get("exp")
            and datetime.utcfromtimestamp(decoded["exp"]) < datetime.utcnow()
        ):
            return None

        return decoded

    except JWTError:
        return None


def check_utilisateur(email: str, mdp: str) -> Optional[int]:
    """
    Vérifie l'email et mot de passe d'un utilisateur.

    Utilisée lors de la connexion pour valider les credentials.

    Parameters
    ----------
    email : str
        L'email de l'utilisateur
    mdp : str
        Le mot de passe en clair

    Returns
    -------
    int or None
        L'ID de l'utilisateur si les credentials sont corrects, None sinon
    """
    try:
        
        utilisateur = user_service.se_connecter(email, mdp)

        if not utilisateur:
            print(f"Email '{email}' introuvable ou mot de passe incorrect")
            return None

        print(f"✅ Connexion réussie pour '{email}' (ID: {utilisateur.id_utilisateur})")
        return utilisateur.id_utilisateur

    except Exception as e:
        print(f"Erreur lors de la vérification : {e}")
        return None


def get_utilisateur_from_token(token: str) -> Optional[dict]:
    """
    Extrait les informations utilisateur depuis un token JWT.

    Utilisée dans les routes protégées pour savoir qui est connecté.

    Parameters
    ----------
    token : str
        Le token JWT

    Returns
    -------
    dict or None
        {
            "id_utilisateur": 1,
            "email": "user@example.com",
            "pseudo": "username",
            "nom": "Nom",
            "prenom": "Prenom"
        }
    """
    
    decoded = decode_jwt(token)

    if not decoded:
        return None

    id_utilisateur = decoded.get("id_utilisateur")

    if not id_utilisateur:
        return None

    
    utilisateur = user_service.user_dao.trouver_par_id(id_utilisateur)

    if not utilisateur:
        return None

    
    return {
        "id_utilisateur": utilisateur.id_utilisateur,
        "email": utilisateur.email,
        "pseudo": utilisateur.pseudo,
        "nom": utilisateur.nom,
        "prenom": utilisateur.prenom,
    }
