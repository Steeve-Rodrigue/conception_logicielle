"""DTO pour les profils"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class ProfileDTO(BaseModel):
    """Profil complet"""

    id_profil: int
    id_utilisateur: int
    titre_professionnel: str
    annees_experience: int
    date_disponibilite: Optional[date]
    type_contrat_recherche: str
    salaire_min_souhaite: Optional[int]
    cv_path: Optional[str]
    linkedin_url: Optional[str]
    taux_completion: float


class ProfileUpdateRequest(BaseModel):
    """Mise à jour profil"""

    titre_professionnel: Optional[str] = Field(None, max_length=150)
    annees_experience: Optional[int] = Field(None, ge=0)
    date_disponibilite: Optional[date] = None
    type_contrat_recherche: Optional[str] = None
    salaire_min_souhaite: Optional[int] = Field(None, ge=0)
    cv_path: Optional[str] = None
    linkedin_url: Optional[str] = None


class ProfileUpdateResponse(BaseModel):
    """Réponse mise à jour"""

    message: str
    champs_modifies: list[str]


class ProfileCompletionResponse(BaseModel):
    """Taux de complétion"""

    id_utilisateur: int
    taux_completion: float
    message: str
