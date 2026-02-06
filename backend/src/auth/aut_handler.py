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

from service.utilisateur_service import UtilisateurService
from utils.security import verify_password

# Charger les variables d'environnement
load_dotenv()

# Configuration JWT
JWT_SECRET = os.getenv("JWT_SECRET", "votre_secret_par_defaut")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", "3600"))

utilisateur_service = UtilisateurService()


def sign_jwt(utilisateur_id: int, est_admin: bool) -> dict:
    """
    Crée un token JWT pour un utilisateur.
    
    Appelée après une connexion réussie pour générer le token.
    
    Parameters
    ----------
    utilisateur_id : int
        ID de l'utilisateur connecté
    est_admin : bool
        True si l'utilisateur est admin
        
    Returns
    -------
    dict
        {
            "access_token": "eyJ0eXAiOiJKV1...",
            "token_type": "bearer"
        }
    """
    # Données à mettre dans le token
    payload = {
        "utilisateur_id": utilisateur_id,
        "est_admin": est_admin,
        "exp": datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    }

    # Créer le token signé
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


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
    # {"utilisateur_id": 1, "est_admin": False, "exp": 1234567890}
    """
    try:
        # Décoder le token
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        # Vérifier l'expiration
        if decoded.get("exp") and datetime.utcfromtimestamp(decoded["exp"]) < datetime.utcnow():
            return None

        return decoded

    except JWTError:
        return None


def check_utilisateur(login: str, mot_de_passe: str) -> Optional[int]:
    """
    Vérifie le login et mot de passe d'un utilisateur.
    
    Utilisée lors de la connexion pour valider les credentials.
    
    Parameters
    ----------
    login : str
        Le login de l'utilisateur
    mot_de_passe : str
        Le mot de passe en clair
        
        
    Returns
    -------
    int or None
        L'ID de l'utilisateur si les credentials sont corrects, None sinon
    """
    try:
        # Chercher l'utilisateur par son login
        utilisateur = utilisateur_service.get_utilisateur_par_login(login)

        if not utilisateur:
            print(f"Login '{login}' introuvable")
            return None

        # Vérifier le mot de passe
        if not verify_password(mot_de_passe, utilisateur.mot_de_passe):
            print(f"Mot de passe incorrect pour '{login}'")
            return None

        print(f"✅ Connexion réussie pour '{login}' (ID: {utilisateur.id_utilisateur})")
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
            "login": "admin",
            "est_admin": True
        }
    """
    # Décoder le token
    decoded = decode_jwt(token)

    if not decoded:
        return None

    utilisateur_id = decoded.get("utilisateur_id")

    if not utilisateur_id:
        return None

    # Récupérer l'utilisateur depuis la base
    utilisateur = utilisateur_service.get_utilisateur_par_id(utilisateur_id)

    if not utilisateur:
        return None

    # Retourner les infos publiques
    return {
        "id_utilisateur": utilisateur.id_utilisateur,
        "login": utilisateur.login,
        "est_admin": utilisateur.est_admin
    }


def verify_admin(token: str) -> bool:
    """
    Vérifie si le token appartient à un admin.
    
    Parameters
    ----------
    token : str
        Le token JWT
        
    Returns
    -------
    bool
        True si admin, False sinon
    """
    decoded = decode_jwt(token)

    if not decoded:
        return False

    return decoded.get("est_admin", False)
