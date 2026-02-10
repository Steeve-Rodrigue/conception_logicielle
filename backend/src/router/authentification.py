"""
Routes d'authentification de l'API.

Expose les endpoints pour la connexion, l'inscription,
la déconnexion et la récupération des informations utilisateur.
Utilise JWT pour la gestion des tokens d'authentification.
"""

from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field, EmailStr, field_validator

from backend.auth.auth_handler import (
    check_utilisateur,
    sign_jwt,
    get_utilisateur_from_token,
)
from backend.auth.auth_bearer import JWTBearer
from backend.utilisateur_service import UtilisateurService


router = APIRouter(
    prefix="/auth",
    tags=["Authentification"],
)


class LoginRequest(BaseModel):
    """Modèle pour les informations de connexion."""

    email: EmailStr = Field(..., description="Email de l'utilisateur")
    mot_de_passe: str = Field(..., description="Mot de passe", min_length=6)

    model_config = {
        "json_schema_extra": {
            "example": {"email": "admin@ensai.fr", "mot_de_passe": "Admin123!"}
        }
    }


class SignupRequest(BaseModel):
    """Modèle pour l'inscription d'un nouvel utilisateur."""

    email: EmailStr = Field(..., description="Email de l'utilisateur")
    mot_de_passe: str = Field(..., description="Mot de passe", min_length=6)
    confirmation_mot_de_passe: str = Field(
        ..., description="Confirmation du mot de passe"
    )
    nom: str = Field(None, description="Nom de famille (optionnel)")
    prenom: str = Field(None, description="Prénom (optionnel)")

    @field_validator("confirmation_mot_de_passe")
    @classmethod
    def passwords_match(cls, v, info):
        """Valide que les deux mots de passe correspondent."""
        if "mot_de_passe" in info.data and v != info.data["mot_de_passe"]:
            raise ValueError("Les mots de passe ne correspondent pas")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@ensai.fr",
                "mot_de_passe": "Test123!",
                "confirmation_mot_de_passe": "Test123!",
                "nom": "Dupont",
                "prenom": "Jean",
            }
        }
    }


class LoginResponse(BaseModel):
    """Modèle pour la réponse de connexion."""

    access_token: str
    token_type: str = "bearer"
    utilisateur: Dict[str, Any]


class MessageResponse(BaseModel):
    """Modèle pour les réponses simples avec message."""

    message: str


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Connexion utilisateur",
    description="Authentifie un utilisateur et retourne un token JWT",
)
async def login(credentials: LoginRequest):
    """
    Authentifie un utilisateur et génère un token JWT.

    Parameters
    ----------
    credentials : LoginRequest
        Email et mot de passe de l'utilisateur

    Returns
    -------
    dict
        Dictionnaire contenant le token d'accès et les infos utilisateur

    Raises
    ------
    HTTPException
        Si les identifiants sont incorrects ou en cas d'erreur
    """
    try:
        utilisateur_id = check_utilisateur(
            email=credentials.email, mot_de_passe=credentials.mot_de_passe
        )

        if not utilisateur_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou mot de passe incorrect",
            )

        utilisateur_service = UtilisateurService()
        utilisateur = utilisateur_service.get_utilisateur_par_id(utilisateur_id)

        if not utilisateur:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé"
            )

        token_data = sign_jwt(
            utilisateur_id=utilisateur.id_utilisateur, est_admin=utilisateur.est_admin
        )

        return {
            "access_token": token_data["access_token"],
            "token_type": "bearer",
            "utilisateur": {
                "id_utilisateur": utilisateur.id_utilisateur,
                "email": utilisateur.email,
                "nom": utilisateur.nom,
                "prenom": utilisateur.prenom,
                "est_admin": utilisateur.est_admin,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'authentification : {e}",
        ) from e


@router.post(
    "/signup",
    response_model=LoginResponse,
    summary="Inscription utilisateur",
    description="Crée un nouveau compte utilisateur et retourne un token JWT",
)
async def signup(user_data: SignupRequest):
    """
    Crée un nouveau compte utilisateur.

    Parameters
    ----------
    user_data : SignupRequest
        Informations d'inscription (email, mot de passe, confirmation, nom, prénom)

    Returns
    -------
    dict
        Dictionnaire contenant le token d'accès et les infos utilisateur

    Raises
    ------
    HTTPException
        Si l'email existe déjà ou si les données sont invalides
    """
    utilisateur_service = UtilisateurService()

    try:
        utilisateur = utilisateur_service.creer_utilisateur(
            email=user_data.email,
            mot_de_passe=user_data.mot_de_passe,
            nom=user_data.nom,
            prenom=user_data.prenom,
            est_admin=False,
        )

        if not utilisateur:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Impossible de créer l'utilisateur (email déjà utilisé ?)",
            )

        token_data = sign_jwt(
            utilisateur_id=utilisateur.id_utilisateur, est_admin=utilisateur.est_admin
        )

        return {
            "access_token": token_data["access_token"],
            "token_type": "bearer",
            "utilisateur": {
                "id_utilisateur": utilisateur.id_utilisateur,
                "email": utilisateur.email,
                "nom": utilisateur.nom,
                "prenom": utilisateur.prenom,
                "est_admin": utilisateur.est_admin,
            },
        }

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve)
        ) from ve

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du compte : {e}",
        ) from e


@router.get(
    "/me",
    response_model=Dict[str, Any],
    summary="Informations utilisateur connecté",
    description="Récupère les informations de l'utilisateur authentifié",
    dependencies=[Depends(JWTBearer())],
)
async def get_current_user(token: str = Depends(JWTBearer())):
    """
    Récupère les informations de l'utilisateur actuellement connecté.

    Parameters
    ----------
    token : str
        Token JWT de l'utilisateur

    Returns
    -------
    dict
        Informations de l'utilisateur connecté

    Raises
    ------
    HTTPException
        Si le token est invalide ou l'utilisateur n'existe plus
    """
    try:
        utilisateur_data = get_utilisateur_from_token(token)

        if not utilisateur_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé"
            )

        return utilisateur_data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des informations : {e}",
        ) from e


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Déconnexion utilisateur",
    description="Déconnecte l'utilisateur (côté client)",
    dependencies=[Depends(JWTBearer())],
)
async def logout():
    """
    Déconnexion de l'utilisateur.

    Note : Avec JWT, la déconnexion est gérée côté client en supprimant le token.

    Returns
    -------
    dict
        Message de confirmation de déconnexion
    """
    return {"message": "Déconnexion réussie. Supprimez le token côté client."}
