import logging
from typing import Optional

from src.business_object.user import User
from src.dao.db_connection import DBConnection
from src.utils.singleton import Singleton


class UserDao(metaclass=Singleton):
    """
    DAO pour la gestion de la persistance des utilisateurs.
    """

    def creer_compte(self, user: User) -> bool:
        """
        Crée un utilisateur dans la base de données.

        Retourne True si succès, False sinon.

        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO utilisateurs (
                            email, pseudo, mot_de_passe_hash, nom, prenom,
                            telephone, date_creation
                        ) VALUES (
                            %(email)s, %(pseudo)s, %(mot_de_passe_hash)s, %(nom)s, %(prenom)s, %(date_creation)s,
                        ) RETURNING id_utilisateur;
                        """,
                        {
                            "email": user.email,
                            "pseudo": user.pseudo,
                            "mot_de_passe_hash": user.mot_de_passe_hash,
                            "nom": user.nom,
                            "prenom": user.prenom,
                            "date_creation": user.date_creation,
                        },
                    )
                    res = cursor.fetchone()
                    if res:
                        user.id_utilisateur = res["id_utilisateur"]
                        return True
        except Exception as e:
            logging.error(f"Erreur création compte: {e}")
        return False

    def trouver_par_email(self, email: str) -> Optional[User]:
        """Recherche un utilisateur par email"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM utilisateurs WHERE email = %(email)s;",
                        {"email": email},
                    )
                    res = cursor.fetchone()
                    if res:
                        return self._row_to_user(res)
        except Exception as e:
            logging.error(f"Erreur recherche par email: {e}")
        return None

    def trouver_par_pseudo(self, pseudo: str) -> Optional[User]:
        """Recherche un utilisateur par pseudo"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM utilisateurs WHERE pseudo = %(pseudo)s;",
                        {"pseudo": pseudo},
                    )
                    res = cursor.fetchone()
                    if res:
                        return self._row_to_user(res)
        except Exception as e:
            logging.error(f"Erreur recherche par pseudo: {e}")
        return None

    def trouver_par_id(self, id_utilisateur: int) -> Optional[User]:
        """Recherche un utilisateur par ID"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM utilisateurs WHERE id_utilisateur = %(id)s;",
                        {"id": id_utilisateur},
                    )
                    res = cursor.fetchone()
                    if res:
                        return self._row_to_user(res)
        except Exception as e:
            logging.error(f"Erreur recherche par ID: {e}")
        return None

    def modifier(self, user: User) -> bool:
        """Modifie un utilisateur existant"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE utilisateurs SET
                            email = %(email)s,
                            pseudo = %(pseudo)s,
                            mot_de_passe_hash = %(mot_de_passe_hash)s,
                            nom = %(nom)s,
                            prenom = %(prenom)s
                        WHERE id_utilisateur = %(id_utilisateur)s;
                        """,
                        {
                            "email": user.email,
                            "pseudo": user.pseudo,
                            "mot_de_passe_hash": user.mot_de_passe_hash,
                            "nom": user.nom,
                            "prenom": user.prenom,
                            "id_utilisateur": user.id_utilisateur,
                        },
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Erreur modification utilisateur: {e}")
        return False

    def supprimer(self, id_utilisateur: int) -> bool:
        """Supprime un utilisateur (CASCADE supprime profil et compétences)"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM utilisateurs WHERE id_utilisateur = %(id)s;",
                        {"id": id_utilisateur},
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Erreur suppression utilisateur: {e}")
        return False

    def mettre_a_jour_derniere_connexion(self, id_utilisateur: int) -> bool:
        """Met à jour la date de dernière connexion"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE utilisateurs
                        SET date_derniere_connexion = CURRENT_TIMESTAMP
                        WHERE id_utilisateur = %(id)s;
                        """,
                        {"id": id_utilisateur},
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Erreur MAJ dernière connexion: {e}")
        return False

    def _row_to_user(row: dict) -> User:
        """Convertit une ligne SQL en objet User"""
        return User(
            id_utilisateur=row["id_utilisateur"],
            email=row["email"],
            pseudo=row["pseudo"],
            mot_de_passe_hash=row["mot_de_passe_hash"],
            nom=row["nom"],
            prenom=row["prenom"],
            date_creation=row["date_creation"],
            date_derniere_connexion=row.get("date_derniere_connexion"),
        )
