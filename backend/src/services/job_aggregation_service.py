import logging
from typing import List

from src.business_object.job_offer import JobOffer
from src.dao.job_offer_dao import JobOfferDao
from src.services.france_travail_service import FranceTravailService


class JobAggregationService:
    """
    Service d'agrégation d'offres d'emploi depuis plusieurs sources.
    """

    def __init__(self):
        self.job_offer_dao = JobOfferDao()
        self.france_travail = FranceTravailService()

    def synchroniser_offres(
        self, mots_cles: str = "développeur", localisation: str = None
    ) -> int:
        """
        Synchronise les offres depuis France Travail vers la BDD locale.

        Returns:
            Nombre d'offres synchronisées
        """
        logging.info(f" Synchronisation des offres : {mots_cles}")

        # Récupérer les offres de France Travail
        offers = self.france_travail.rechercher_offres(
            mots_cles=mots_cles, localisation=localisation
        )

        # Sauvegarder en BDD (UPSERT)
        count = 0
        for offer in offers:
            if self.job_offer_dao.creer_offre(offer):
                count += 1

        logging.info(f"{count} offres synchronisées")
        return count

    def rechercher_offres_locales(
        self,
        mots_cles: str = None,
        localisation: str = None,
        type_contrat: str = None,
        competences: List[str] = None,
        limit: int = 100,
    ) -> List[JobOffer]:
        """Recherche des offres dans la BDD locale"""
        return self.job_offer_dao.rechercher_offres(
            mots_cles=mots_cles,
            localisation=localisation,
            type_contrat=type_contrat,
            competences=competences,
            limit=limit,
        )
