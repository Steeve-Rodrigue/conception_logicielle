import logging
from typing import Optional
from datetime import datetime, date, timedelta

from src.business_object.user import User
from src.dao.user_dao import UserDao
from src.services.profile_service import ProfileService
from src.utils.security import (
    hash_password,
    verify_password,
    validate_password_strength,
)


class UserService:
    """
    Service orchestrant la logique applicative des utilisateurs.
    """

    def __init__(self):
        self.user_dao = UserDao()
        self.profile_service = ProfileService()

    def creer_utilisateur(
        self,
        email: str,
        pseudo: str,
        mdp: str,
        nom: str,
        prenom: str,
    ) -> Optional[User]:
        """
        Crée un utilisateur avec validation complète.
        """
        # 1. Validation format email
        user_temp = User(
            email=email,
            pseudo=pseudo,
            mdp_hash="",
            nom=nom,
            prenom=prenom,
        )
        if not user_temp.valider_email():
            logging.error(f"Email invalide: {email}")
            return None

        is_valid, message = validate_password_strength(mdp)
        if not is_valid:
            logging.error(f"Mot de passe invalide: {message}")
            return None

        # Vérification unicité email et pseudo
        if self.email_deja_utilise(email):
            logging.error(f"Email déjà utilisé: {email}")
            return None
        if self.pseudo_deja_utilise(pseudo):
            logging.error(f"Pseudo déjà utilisé: {pseudo}")
            return None

        # Hashage du mot de passe
        mot_de_passe_hash = hash_password(mdp)

        # Création de l'utilisateur
        user = User(
            email=email,
            pseudo=pseudo,
            mdp_hash=mot_de_passe_hash,
            nom=nom,
            prenom=prenom,
            date_creation=datetime.now(),
        )

        if self.user_dao.creer_compte(user):
            # Création automatique d'un profil vide
            self.profile_service.creer_profil(
                id_utilisateur=user.id_utilisateur,
                titre_professionnel="Non renseigné",
                annees_experience=0,
                date_disponibilite=date.today() + timedelta(days=30),
                type_contrat_recherche="CDI",
            )
            return user
        return None

    def se_connecter(self, email: str, mdp: str) -> Optional[User]:
        """
        Authentifie un utilisateur par email et mot de passe.
        """
        user = self.user_dao.trouver_par_email(email)
        if not user:
            logging.warning(f"Tentative de connexion échouée pour email: {email}")
            return None

        # Vérification du mot de passe
        if verify_password(mdp, user.mdp_hash):
            self.user_dao.mettre_a_jour_derniere_connexion(user.id_utilisateur)
            return user

        logging.warning(f"Mot de passe incorrect pour: {email}")
        return None

    def modifier_utilisateur(
        self,
        id_utilisateur: int,
        email: Optional[str] = None,
        pseudo: Optional[str] = None,
        nom: Optional[str] = None,
        prenom: Optional[str] = None,
    ) -> bool:
        """Modifie les informations d'un utilisateur"""
        user = self.user_dao.trouver_par_id(id_utilisateur)
        if not user:
            return False

        # Mise à jour des champs fournis
        if email and email != user.email:
            # Validation email
            user_temp = User(
                email=email, pseudo="temp", mot_de_passe_hash="", nom="", prenom=""
            )
            if not user_temp.valider_email():
                logging.error(f"Email invalide: {email}")
                return False

            if self.email_deja_utilise(email):
                logging.error(f"Email déjà utilisé: {email}")
                return False
            user.email = email

        if pseudo and pseudo != user.pseudo:
            if self.pseudo_deja_utilise(pseudo):
                logging.error(f"Pseudo déjà utilisé: {pseudo}")
                return False
            user.pseudo = pseudo

        if nom:
            user.nom = nom
        if prenom:
            user.prenom = prenom

        return self.user_dao.modifier(user)

    def changer_mot_de_passe(
        self, id_utilisateur: int, ancien_mdp: str, nouveau_mdp: str
    ) -> bool:
        """Change le mot de passe d'un utilisateur"""
        user = self.user_dao.trouver_par_id(id_utilisateur)
        if not user:
            return False

        # Vérification ancien mot de passe
        if not verify_password(ancien_mdp, user.mot_de_passe_hash):
            logging.error("Ancien mot de passe incorrect")
            return False

        # Validation nouveau mot de passe
        is_valid, message = validate_password_strength(nouveau_mdp)
        if not is_valid:
            logging.error(f"Nouveau mot de passe invalide: {message}")
            return False

        # Mise à jour avec nouveau hash
        user.mdp_hash = hash_password(nouveau_mdp)
        return self.user_dao.modifier(user)

    def supprimer_utilisateur(self, id_utilisateur: int) -> bool:
        """
        Supprime un utilisateur (CASCADE supprime profil et compétences).
        """
        return self.user_dao.supprimer(id_utilisateur)

    def email_deja_utilise(self, email: str) -> bool:
        """Vérifie si l'email existe déjà"""
        return self.user_dao.trouver_par_email(email) is not None

    def pseudo_deja_utilise(self, pseudo: str) -> bool:
        """Vérifie si le pseudo existe déjà"""
        return self.user_dao.trouver_par_pseudo(pseudo) is not None
