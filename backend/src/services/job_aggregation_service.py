"""Service d'agrégation d'offres d'emploi"""

from typing import List, Optional

from src.business_object.job_offer import JobOffer
from src.dao.job_offer_dao import JobOfferDao
from src.services.france_travail_service import FranceTravailService
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class JobAggregationService:
    """Service d'agrégation d'offres d'emploi depuis plusieurs sources"""

    def __init__(self):
        self.job_offer_dao = JobOfferDao()
        self.france_travail = FranceTravailService()

    def synchroniser_offres(
        self, termes: List[str], departement: Optional[str] = None
    ) -> int:
        """
        Synchronise les offres depuis France Travail vers la BDD locale

        Args:
            termes: Liste de mots-clés (ex: ["data scientist", "ML"])
            departement: Code département optionnel

        Returns:
            Nombre d'offres synchronisées
        """
        logger.info(f" Synchronisation pour {len(termes)} termes")

        count_total = 0
        offres_vues = set()  # Pour éviter les doublons entre termes

        for terme in termes:
            logger.info(f"🔎 Terme: '{terme}'")

            # Rechercher les offres
            offers: List[JobOffer] = self.france_travail.rechercher_offres(
                mots_cles=terme, departement=departement
            )

            # Sauvegarder en base (avec déduplication)
            count_terme = 0
            for offer in offers:
                if offer.external_id not in offres_vues:
                    if self.job_offer_dao.creer_offre(offer):
                        count_terme += 1
                        offres_vues.add(offer.external_id)

            logger.info(f"   → {count_terme} nouvelles offres pour '{terme}'")
            count_total += count_terme

        logger.info(f"Total synchronisé: {count_total} offres")
        return count_total

    def rechercher_offres_locales(
        self,
        mots_cles: Optional[str] = None,
        localisation: Optional[str] = None,
        type_contrat: Optional[str] = None,
        competences: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[JobOffer]:
        """Recherche des offres dans la BDD locale"""
        return self.job_offer_dao.rechercher_offres(
            mots_cles=mots_cles,
            localisation=localisation,
            type_contrat=type_contrat,
            competences=competences,
            limit=limit,
            offset=offset,
        )
