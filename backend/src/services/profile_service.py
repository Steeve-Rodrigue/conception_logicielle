import logging
from typing import Optional, List

from business_object.candidate_profile import CandidateProfile
from business_object.user_skill import UserSkill
from dao.profile_dao import ProfileDao
from dao.skill_dao import SkillDao


class ProfileService:
    """
    SERVICE : Orchestre la logique applicative des profils candidats.
    """

    def __init__(self):
        self.profile_dao = ProfileDao()
        self.skill_dao = SkillDao()

    def creer_profil(
        self,
        id_utilisateur: int,
        titre_professionnel: str,
        annees_experience: int = 0,
        disponibilite: str = "Immédiate",
        type_contrat_recherche: str = "CDI",
        **kwargs,
    ) -> Optional[CandidateProfile]:
        """
        Crée un profil candidat.
        """

        # Création de l'objet Business
        profile = CandidateProfile(
            id_utilisateur=id_utilisateur,
            titre_professionnel=titre_professionnel,
            annees_experience=annees_experience,
            disponibilite=disponibilite,
            type_contrat_recherche=type_contrat_recherche,
            **kwargs,
        )

        # Validation
        if annees_experience < 0:
            logging.error("Années d'expérience invalides")
            return None

        # Persistance via DAO
        if self.profile_dao.creer_profil(profile):
            logging.info(f"Profil créé pour utilisateur {id_utilisateur}")
            return profile

        logging.error("Échec création profil")
        return None

    def obtenir_profil_utilisateur(
        self, id_utilisateur: int
    ) -> Optional[CandidateProfile]:
        """Récupère le profil d'un utilisateur"""
        return self.profile_dao.obtenir_profil_par_utilisateur(id_utilisateur)

    def mettre_a_jour_profil(self, id_utilisateur: int, **kwargs) -> bool:
        """
        Met à jour le profil d'un utilisateur.
        """
        # Récupération du profil existant
        profile = self.profile_dao.obtenir_profil_par_utilisateur(id_utilisateur)
        if not profile:
            logging.error(f"Profil introuvable pour utilisateur {id_utilisateur}")
            return False

        # Mise à jour des champs fournis
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)

        # Persistance
        return self.profile_dao.mettre_a_jour_profil(profile)

    def ajouter_competence(
        self, id_profil: int, nom_competence: str, niveau: str, categorie: str
    ) -> bool:
        """Ajoute une compétence au profil"""
        # Vérification doublon
        if self.skill_dao.competence_existe(id_profil, nom_competence):
            logging.warning(f"Compétence '{nom_competence}' déjà présente")
            return False

        # Création de l'objet UserSkill
        skill = UserSkill(
            id_profil=id_profil,
            nom_competence=nom_competence,
            niveau=niveau,
            categorie=categorie,
        )

        # Validation
        if not skill.valider_niveau():
            logging.error(f"Niveau invalide: {niveau}")
            return False

        # Persistance
        return self.skill_dao.ajouter_competence(skill)

    def lister_competences(self, id_profil: int) -> List[UserSkill]:
        """Liste toutes les compétences d'un profil"""
        return self.skill_dao.lister_competences_utilisateur(id_profil)

    def supprimer_competence(self, id_user_skill: int) -> bool:
        """Supprime une compétence"""
        return self.skill_dao.supprimer_competence(id_user_skill)
