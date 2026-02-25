from typing import Optional

from src.business_object.candidate_profile import CandidateProfile
from src.dao.db_connection import DBConnection
from src.utils.singleton import Singleton
from src.utils.logger import setup_logger


logger = setup_logger(__name__)


class ProfileDao(metaclass=Singleton):
    """
    DAO pour la gestion des profils candidats.
    """

    def creer_profil(self, profile: CandidateProfile) -> bool:
        """Crée un profil candidat"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO candidate_profile (
                            id_utilisateur, titre_professionnel, annees_experience,
                            date_disponibilite, type_contrat_recherche, salaire_min_souhaite,
                            cv_path, linkedin_url
                        ) VALUES (
                            %(id_utilisateur)s, %(titre_professionnel)s, %(annees_experience)s,
                            %(date_disponibilite)s, %(type_contrat_recherche)s, %(salaire_min_souhaite)s,
                            %(cv_path)s, %(linkedin_url)s
                        ) RETURNING id_profil;
                        """,
                        {
                            "id_utilisateur": profile.id_utilisateur,
                            "titre_professionnel": profile.titre_professionnel,
                            "annees_experience": profile.annees_experience,
                            "date_disponibilite": profile.date_disponibilite,
                            "type_contrat_recherche": profile.type_contrat_recherche,
                            "salaire_min_souhaite": profile.salaire_min_souhaite,
                            "cv_path": profile.cv_path,
                            "linkedin_url": profile.linkedin_url,
                        },
                    )
                    res = cursor.fetchone()
                    if res:
                        profile.id_profil = res["id_profil"]
                        return True
        except Exception as e:
            logger.error(f"Erreur création profil: {e}")
        return False

    def obtenir_profil_par_utilisateur(
        self, id_utilisateur: int
    ) -> Optional[CandidateProfile]:
        """Récupère le profil d'un utilisateur"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM candidate_profile WHERE id_utilisateur = %(id)s;",
                        {"id": id_utilisateur},
                    )
                    res = cursor.fetchone()
                    if res:
                        return self._row_to_profile(res)
        except Exception as e:
            logger.error(f"Erreur récupération profil: {e}")
        return None

    def mettre_a_jour_profil(self, profile: CandidateProfile) -> bool:
        """Met à jour un profil existant"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE candidate_profile SET
                            titre_professionnel = %(titre_professionnel)s,
                            annees_experience = %(annees_experience)s,
                            date_disponibilite = %(date_disponibilite)s,
                            type_contrat_recherche = %(type_contrat_recherche)s,
                            salaire_min_souhaite = %(salaire_min_souhaite)s,
                            cv_path = %(cv_path)s,
                            linkedin_url = %(linkedin_url)s
                        WHERE id_profil = %(id_profil)s;
                        """,
                        {
                            "titre_professionnel": profile.titre_professionnel,
                            "annees_experience": profile.annees_experience,
                            "date_disponibilite": profile.date_disponibilite,
                            "type_contrat_recherche": profile.type_contrat_recherche,
                            "salaire_min_souhaite": profile.salaire_min_souhaite,
                            "cv_path": profile.cv_path,
                            "linkedin_url": profile.linkedin_url,
                            "id_profil": profile.id_profil,
                        },
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Erreur MAJ profil: {e}")
        return False

    def _row_to_profile(self, row: dict) -> CandidateProfile:
        """Convertit une ligne SQL en objet CandidateProfile"""
        return CandidateProfile(
            id_profil=row["id_profil"],
            id_utilisateur=row["id_utilisateur"],
            titre_professionnel=row["titre_professionnel"],
            annees_experience=row["annees_experience"],
            date_disponibilite=row["date_disponibilite"],
            type_contrat_recherche=row["type_contrat_recherche"],
            salaire_min_souhaite=row.get("salaire_min_souhaite"),
            cv_path=row.get("cv_path"),
            linkedin_url=row.get("linkedin_url"),
            date_maj=row["date_maj"],
        )
