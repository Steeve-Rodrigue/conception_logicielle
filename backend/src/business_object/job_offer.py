from datetime import datetime
from typing import Optional, List


class JobOffer:
    """
    Business Object représentant une offre d'emploi.
    """

    def __init__(
        self,
        external_id: str,
        titre: str,
        entreprise: str,
        description: str,
        localisation: str,
        type_contrat: str,
        salaire: Optional[str] = None,
        competences_requises: Optional[List[str]] = None,
        date_publication: Optional[datetime] = None,
        url_origine: Optional[str] = None,
        source: str = "france_travail",
        id_offre: Optional[int] = None,
        est_active: bool = True,
        date_maj: Optional[datetime] = None,
    ):
        self.id_offre = id_offre
        self.external_id = external_id
        self.titre = titre
        self.entreprise = entreprise
        self.description = description
        self.localisation = localisation
        self.type_contrat = type_contrat
        self.salaire = salaire
        self.competences_requises = competences_requises or []
        self.date_publication = date_publication or datetime.now()
        self.url_origine = url_origine
        self.source = source
        self.est_active = est_active
        self.date_maj = date_maj or datetime.now()

    def to_dict(self) -> dict:
        """Convertit l'offre en dictionnaire"""
        return {
            "id_offre": self.id_offre,
            "external_id": self.external_id,
            "titre": self.titre,
            "entreprise": self.entreprise,
            "description": self.description,
            "localisation": self.localisation,
            "type_contrat": self.type_contrat,
            "salaire": self.salaire,
            "competences_requises": self.competences_requises,
            "date_publication": (
                self.date_publication.isoformat() if self.date_publication else None
            ),
            "url_origine": self.url_origine,
            "source": self.source,
            "est_active": self.est_active,
            "date_maj": self.date_maj.isoformat() if self.date_maj else None,
        }
