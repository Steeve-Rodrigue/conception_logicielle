"""
DTOs pour les routes d'authentification.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator


class LoginRequest(BaseModel):
    """Modèle pour les informations de connexion."""

    email: EmailStr
    mdp: str = Field(..., min_length=6)


class SignupRequest(BaseModel):
    """Modèle pour l'inscription d'un nouvel utilisateur."""

    email: EmailStr
    pseudo: str = Field(..., min_length=3)
    mdp: str = Field(..., min_length=6)
    confirmation_mdp: str
    nom: str
    prenom: str

    @field_validator("confirmation_mdp")
    @classmethod
    def passwords_match(cls, v, info):
        if "mdp" in info.data and v != info.data["mdp"]:
            raise ValueError("Les mots de passe ne correspondent pas")
        return v


class UtilisateurResponse(BaseModel):
    """Infos utilisateur retournées dans les réponses."""

    id_utilisateur: int
    email: str
    pseudo: str
    nom: str
    prenom: str


class LoginResponse(BaseModel):
    """Réponse de connexion avec token JWT."""

    access_token: str
    token_type: str = "bearer"
    utilisateur: UtilisateurResponse


class MessageResponse(BaseModel):
    """Réponse simple avec message."""

    message: str
