import logging
from typing import List, Optional

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
        self, termes: List[str], departement: Optional[str] = None
    ) -> int:
        """
        Synchronise les offres depuis France Travail vers la BDD locale
        pour une liste de termes et un département optionnel.

        Args:
            termes: Liste de mots-clés (ex: ["data scientist", "ML"])
            departement: Code département optionnel

        Returns:
            Nombre d'offres synchronisées
        """
        logging.info(f" Synchronisation des offres pour {len(termes)} termes")

        count_total = 0

        for terme in termes:
            logging.info(f"  Recherche pour le terme : {terme}")
            offers: List[JobOffer] = self.france_travail.rechercher_toutes_offres(
                mots_cles=terme, departement=departement
            )
            count_terme = 0
            for offer in offers:
                if self.job_offer_dao.creer_offre(offer):
                    count_terme += 1
            logging.info(f"    {count_terme} nouvelles offres pour '{terme}'")
            count_total += count_terme

        logging.info(f"Total synchronisé : {count_total} offres")
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
