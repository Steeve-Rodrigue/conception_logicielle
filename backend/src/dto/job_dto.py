"""DTO pour les offres d'emploi"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class JobOfferDTO(BaseModel):
    """DTO pour une offre d'emploi"""
    id_offre: int
    external_id: str
    titre: str
    entreprise: str
    description: str
    localisation: str
    type_contrat: str
    salaire: Optional[str] = None
    competences_requises: List[str] = []
    url_origine: Optional[str] = None
    date_publication: datetime
    source: str
    est_active: bool

    class Config:
        from_attributes = True


class JobSearchResponse(BaseModel):
    """Réponse pour la recherche d'offres"""
    total: int
    results: List[JobOfferDTO]



class SyncRequest(BaseModel):
    termes: Optional[List[str]] = Field(
        None,
        description="Liste de termes à rechercher"
    )
    departement: Optional[str] = Field(
        None,
        description="Code département"
    )


class SyncResponse(BaseModel):
    """Réponse de synchronisation"""
    status: str
    message: str