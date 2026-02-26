"""
Gestion des tokens JWT et authentification.
Ce fichier contient toutes les fonctions pour :
- Créer un token JWT quand quelqu'un se connecte
- Vérifier un token JWT
- Vérifier un login/mot de passe
- Extraire les infos d'un token
"""
import os
import logging
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from dotenv import load_dotenv

from src.services.user_service import UserService
from src.authentication_dto import UtilisateurResponse

load_dotenv()

logger = logging.getLogger(__name__)

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
            logger.warning("Email '%s' introuvable ou mot de passe incorrect", email)
            return None
        logger.info("Connexion réussie pour '%s' (ID: %s)", email, utilisateur.id_utilisateur)
        return utilisateur.id_utilisateur
    except Exception as e:
        logger.error("Erreur lors de la vérification : %s", e)
        return None


def get_utilisateur_from_token(token: str) -> Optional[UtilisateurResponse]:
    """
    Extrait les informations utilisateur depuis un token JWT.
    Utilisée dans les routes protégées pour savoir qui est connecté.

    Parameters
    ----------
    token : str
        Le token JWT

    Returns
    -------
    UtilisateurResponse or None
        Les informations de l'utilisateur si le token est valide, None sinon
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

    return UtilisateurResponse(
        id_utilisateur=utilisateur.id_utilisateur,
        email=utilisateur.email,
        pseudo=utilisateur.pseudo,
        nom=utilisateur.nom,
        prenom=utilisateur.prenom,
    )
