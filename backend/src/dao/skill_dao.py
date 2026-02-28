from typing import List

from src.business_object.user_skill import UserSkill
from src.dao.db_connection import DBConnection
from src.utils.singleton import Singleton
from src.utils.logger import setup_logger


logger = setup_logger(__name__)


class SkillDao(metaclass=Singleton):
    """
    DAO pour la gestion des compétences utilisateur.
    """

    def ajouter_competence(self, skill: UserSkill) -> bool:
        """Ajoute une compétence à un profil"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO user_skill (
                            id_profil, nom_competence, niveau, categorie
                        ) VALUES (
                            %(id_profil)s, %(nom_competence)s, %(niveau)s, %(categorie)s
                        ) RETURNING id_user_skill;
                        """,
                        {
                            "id_profil": skill.id_profil,
                            "nom_competence": skill.nom_competence,
                            "niveau": skill.niveau,
                            "categorie": skill.categorie,
                        },
                    )
                    res = cursor.fetchone()
                    if res:
                        skill.id_user_skill = res["id_user_skill"]
                        return True
        except Exception as e:
            logger.error(f"Erreur ajout compétence: {e}")
        return False

    def lister_competences_utilisateur(self, id_profil: int) -> List[UserSkill]:
        """Liste toutes les compétences d'un profil"""
        competences = []
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM user_skill WHERE id_profil = %(id)s ORDER BY nom_competence;",
                        {"id": id_profil},
                    )
                    rows = cursor.fetchall()
                    for row in rows:
                        competences.append(self._row_to_skill(row))
        except Exception as e:
            logger.error(f"Erreur liste compétences: {e}")
        return competences

    def supprimer_competence(self, id_user_skill: int) -> bool:
        """Supprime une compétence"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM user_skill WHERE id_user_skill = %(id)s;",
                        {"id": id_user_skill},
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Erreur suppression compétence: {e}")
        return False

    def competence_existe(self, id_profil: int, nom_competence: str) -> bool:
        """Vérifie si une compétence existe déjà pour un profil"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 1 FROM user_skill 
                        WHERE id_profil = %(id_profil)s 
                        AND nom_competence = %(nom_competence)s;
                        """,
                        {"id_profil": id_profil, "nom_competence": nom_competence},
                    )
                    return cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"Erreur: la compétence existe déjà: {e}")
        return False

    def _row_to_skill(self, row: dict) -> UserSkill:
        """Convertit une ligne SQL en objet UserSkill"""
        return UserSkill(
            id_user_skill=row["id_user_skill"],
            id_profil=row["id_profil"],
            nom_competence=row["nom_competence"],
            niveau=row["niveau"],
            categorie=row["categorie"],
        )
