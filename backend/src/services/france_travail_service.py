"""Service France Travail - Version propre et corrigée"""

import os
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

from src.business_object.job_offer import JobOffer
from src.utils.logger import setup_logger
from src.utils.tech_keywords import TECH_KEYWORDS

load_dotenv()
logger = setup_logger(__name__)


class FranceTravailService:
    """Service de connexion à l'API France Travail"""

    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID_FRANCE_TRAVAIL")
        self.client_secret = os.getenv("CLIENT_SECRET_FRANCE_TRAVAIL")

        if not self.client_id or not self.client_secret:
            logger.warning(" Credentials France Travail manquants")

        self.url_auth = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire"
        self.url_search = (
            "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
        )
        self.token = None

    def _obtenir_token(self):
        """Récupère le token OAuth2"""
        if self.token:
            return self.token

        donnees = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "api_offresdemploiv2 o2dsoffre",
        }

        try:
            response = requests.post(self.url_auth, data=donnees, timeout=10)
            response.raise_for_status()
            self.token = response.json().get("access_token")
            logger.info(" Token OAuth2 obtenu")
            return self.token
        except Exception as e:
            logger.error(f"Erreur authentification: {e}")
            return None

    def rechercher_offres(
        self,
        mots_cles: str = "data scientist",
        departement: str = None,
        limit: int = 150,
    ):
        """
        Recherche des offres avec pagination automatique

        Args:
            mots_cles: Termes de recherche
            departement: Code département (optionnel)
            limit: Nombre max d'offres (max 1000)

        Returns:
            Liste d'objets JobOffer
        """
        toutes_offres = []
        batch_size = 150
        offset = 0

        while offset < limit:
            offres_batch = self._rechercher_batch(
                mots_cles, departement, offset, batch_size
            )

            if not offres_batch:
                break

            toutes_offres.extend(offres_batch)
            offset += len(offres_batch)

            if len(offres_batch) < batch_size:
                break

            if offset >= 1000:
                logger.warning(" Limite API (1000) atteinte")
                break

            time.sleep(0.5)

        return toutes_offres

    def _rechercher_batch(
        self, mots_cles: str, departement: str, offset: int, limit: int
    ):
        """Recherche un batch d'offres"""
        token = self._obtenir_token()
        if not token:
            return []

        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

        params = {"motsCles": mots_cles, "range": f"{offset}-{offset + limit - 1}"}

        if departement:
            params["departement"] = departement

        try:
            response = requests.get(
                self.url_search, headers=headers, params=params, timeout=15
            )

            if response.status_code in [204, 416]:
                return []

            if response.status_code not in [200, 206]:
                logger.error(f"Status {response.status_code}: {response.text[:200]}")
                return []

            data = response.json()
            offres_json = data.get("resultats", [])

            return [self._parse_offre(offre) for offre in offres_json]

        except Exception as e:
            logger.error(f" Erreur batch offset={offset}: {e}")
            return []

    def _parse_offre(self, data: dict) -> JobOffer:
        """
        Parse une offre JSON de l'API → JobOffer

        Args:
            data: Dictionnaire JSON d'une offre

        Returns:
            Objet JobOffer
        """
        description = data.get("description", "") or ""
        competences_brutes = data.get("competences", [])
        competences = [
            comp.get("libelle")
            for comp in competences_brutes
            if isinstance(comp, dict) and comp.get("libelle")
        ]

        if not competences:
            competences = [
                mot for mot in TECH_KEYWORDS if mot.lower() in description.lower()
            ]

        origine = data.get("origineOffre", {})
        url = origine.get("urlOrigine") if isinstance(origine, dict) else None

        salaire_data = data.get("salaire", {})
        salaire = (
            salaire_data.get("libelle", "Non renseigné")
            if isinstance(salaire_data, dict)
            else "Non renseigné"
        )

        date_creation_str = data.get("dateCreation")
        date_pub = self._parse_date(date_creation_str)

        date_maj_str = data.get("dateActualisation")
        date_maj = self._parse_date(date_maj_str)

        return JobOffer(
            external_id=data.get("id"),
            titre=data.get("intitule", "Sans titre"),
            entreprise=data.get("entreprise", {}).get("nom", "Non renseigné"),
            description=data.get("description", ""),
            localisation=data.get("lieuTravail", {}).get("libelle", "France"),
            type_contrat=data.get("typeContratLibelle", data.get("typeContrat", "NC")),
            salaire=salaire,
            competences_requises=competences,
            date_publication=date_pub,
            date_maj=date_maj,
            url_origine=url,
            source="france_travail",
        )

    @staticmethod
    def _parse_date(date_str: str) -> datetime:
        """Parse une date ISO 8601"""
        if not date_str:
            return datetime.now()

        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except Exception:
            return datetime.now()
