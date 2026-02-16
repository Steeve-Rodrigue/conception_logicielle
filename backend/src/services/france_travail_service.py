"""Service France Travail - Récupération complète des offres"""

import os
import requests
import logging
import re
import time
from typing import List
from src.business_object.job_offer import JobOffer
from src.dao.job_offer_dao import JobOfferDao
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
jobOfferDao = JobOfferDao()


class FranceTravailService:
    """Service de connexion à l'API France Travail"""

    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID_FRANCE_TRAVAIL")
        self.client_secret = os.getenv("CLIENT_SECRET_FRANCE_TRAVAIL")
        self.url_authentification = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire"
        self.url_recherche = (
            "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
        )
        self.token = None

    def _obtenir_badge_acces(self):
        """Récupère le token OAuth2 (avec cache)"""
        if self.token:
            return self.token

        donnees = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "api_offresdemploiv2 o2dsoffre",
        }
        try:
            reponse = requests.post(self.url_authentification, data=donnees, timeout=10)
            reponse.raise_for_status()
            self.token = reponse.json().get("access_token")
            return self.token
        except Exception as e:
            logger.error(f"❌ Erreur authentification: {e}")
            return None

    def rechercher_toutes_offres(
        self, mots_cles="data scientist statistiques ", departement=None
    ):
        """

        Args:
            mots_cles: Termes de recherche (ex: "data scientist", "développeur python")
            departement: Code département optionnel (ex: "35")
        """
        toutes_offres = []
        batch_size = 150  # Max par requête
        offset = 0
        total_recupere = 0

        logger.info(
            f"🔍 Recherche globale: '{mots_cles}' {f'(dept: {departement})' if departement else ''}"
        )

        while True:
            # Récupérer un batch
            offres_batch = self._rechercher_batch(
                mots_cles=mots_cles,
                departement=departement,
                offset=offset,
                limit=batch_size,
            )

            if not offres_batch:
                logger.info(f" Fin de la pagination - Total: {total_recupere} offres")
                break

            toutes_offres.extend(offres_batch)
            total_recupere += len(offres_batch)
            offset += batch_size

            logger.info(
                f" Batch {offset // batch_size}: {len(offres_batch)} offres (Total: {total_recupere})"
            )

            # Si on reçoit moins que le batch_size, c'est la dernière page
            if len(offres_batch) < batch_size:
                logger.info(f" Dernière page atteinte - Total: {total_recupere} offres")
                break

            # Limite de sécurité (France Travail limite à ~1000 résultats)
            if offset >= 1000:
                logger.warning("Limite de 1000 offres atteinte (limite API)")
                break

            # Petit délai pour ne pas surcharger l'API
            time.sleep(0.5)

        return toutes_offres

    def _rechercher_batch(self, mots_cles, departement, offset, limit):
        """Recherche un batch d'offres (une page)"""
        badge = self._obtenir_badge_acces()
        if not badge:
            return []

        entetes = {"Authorization": f"Bearer {badge}", "Accept": "application/json"}

        parametres = {"motsCles": mots_cles, "range": f"{offset}-{offset + limit - 1}"}

        # Ajouter le département si spécifié
        if departement:
            parametres["departement"] = departement

        try:
            reponse = requests.get(
                self.url_recherche, headers=entetes, params=parametres, timeout=15
            )

            if reponse.status_code == 204:
                return []

            if reponse.status_code == 416:  # Range Not Satisfiable (plus d'offres)
                return []

            reponse.raise_for_status()
            offres_json = reponse.json().get("resultats", [])

            return [self._transformer_en_objet(off) for off in offres_json]

        except Exception as e:
            logger.error(f"Erreur batch offset={offset}: {e}")
            return []

    def rechercher_offres_multiples_termes(
        self, liste_termes: List[str], departement=None
    ):
        """
        Recherche avec plusieurs termes pour couvrir plus d'offres.

        Args:
            liste_termes: Liste de termes (ex: ["data scientist", "data analyst", "machine learning"])
            departement: Code département optionnel

        Returns:
            Liste d'offres (dédupliquées par external_id)
        """
        toutes_offres = []
        offres_vues = set()  # Pour éviter les doublons

        for terme in liste_termes:
            logger.info(f"\n🔎 Recherche avec le terme: '{terme}'")
            offres = self.rechercher_toutes_offres(
                mots_cles=terme, departement=departement
            )

            # Filtrer les doublons
            nouvelles_offres = 0
            for offre in offres:
                if offre.external_id not in offres_vues:
                    toutes_offres.append(offre)
                    offres_vues.add(offre.external_id)
                    nouvelles_offres += 1

            logger.info(
                f"   → {nouvelles_offres} nouvelles offres ({len(offres) - nouvelles_offres} doublons ignorés)"
            )

        logger.info(f"\n✅ TOTAL FINAL: {len(toutes_offres)} offres uniques")
        return toutes_offres

    def _transformer_en_objet(self, data):
        """Transforme JSON → JobOffer"""

        # Extraction des compétences
        competences_brutes = data.get("competences", [])
        liste_competences = [
            comp.get("libelle")
            for comp in competences_brutes
            if isinstance(comp, dict) and comp.get("libelle")
        ]

        # Si pas de compétences, extraire de la description
        if not liste_competences:
            description = data.get("description", "")
            mots_cles_tech = [
                "Python",
                "Java",
                "JavaScript",
                "React",
                "Angular",
                "Docker",
                "Kubernetes",
                "AWS",
                "Azure",
                "SQL",
                "Git",
                "TensorFlow",
                "PyTorch",
                "Scikit-learn",
                "Pandas",
                "R",
            ]
            liste_competences = [mot for mot in mots_cles_tech if mot in description]

        # Extraction de l'URL
        origine_offre = data.get("origineOffre", {})
        url_postuler = (
            origine_offre.get("urlOrigine") if isinstance(origine_offre, dict) else None
        )

        if not url_postuler:
            contact = data.get("contact", {})
            if isinstance(contact, dict):
                coordonnees = contact.get("coordonnees1", "")
                if "https://" in coordonnees:
                    urls = re.findall(r"https://[^\s]+", coordonnees)
                    url_postuler = urls[0] if urls else None

        return JobOffer(
            external_id=data.get("id"),
            titre=data.get("intitule", "Sans titre"),
            salaire=data.get("salaire", {}).get("libelle", "Non renseigné"),
            entreprise=data.get("entreprise", {}).get("nom", "Non renseigné"),
            description=data.get("description", ""),
            localisation=data.get("lieuTravail", {}).get("libelle", "France"),
            type_contrat=data.get("typeContratLibelle", data.get("typeContrat", "NC")),
            competences_requises=liste_competences,
            url_origine=url_postuler,
            source="france_travail",
        )


# ========================================
# TEST
# ========================================
if __name__ == "__main__":
    service = FranceTravailService()

    # Recherche avec plusieurs termes (plus d'offres)
    print("\n" + "=" * 80)
    print("🔍 RECHERCHE MULTIPLE TERMES")
    print("=" * 80)
    termes = [
        "data scientist",
        "data analyst",
        "machine learning ",
        "ML",
        "Statistiques",
        "LMM",
    ]
    offres_multiples = service.rechercher_offres_multiples_termes(termes)
    print(f"\n✅ {len(offres_multiples)} offres uniques au total\n")

    for offre in offres_multiples:
        jobOfferDao.creer_offre(offre)

    print(f"\n✅ {len(offres_multiples)} offres uniques au total sauvegardées\n")
