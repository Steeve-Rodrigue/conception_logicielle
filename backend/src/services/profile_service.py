from datetime import date
from typing import Optional, List

from src.business_object.candidate_profile import CandidateProfile
from src.business_object.user_skill import UserSkill
from src.dao.profile_dao import ProfileDao
from src.dao.skill_dao import SkillDao
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

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
        annees_experience: int,
        date_disponibilite: date,
        type_contrat_recherche: str,
        salaire_min_souhaite: Optional[int] = None,
        cv_path: Optional[str] = None,
        linkedin_url: Optional[str] = None,
    ) -> Optional[CandidateProfile]:
        """
        Crée un profil candidat.
        """

        try:
            profile = CandidateProfile(
                id_utilisateur=id_utilisateur,
                titre_professionnel=titre_professionnel,
                annees_experience=annees_experience,
                date_disponibilite=date_disponibilite,
                type_contrat_recherche=type_contrat_recherche,
                salaire_min_souhaite=salaire_min_souhaite,
                cv_path=cv_path,
                linkedin_url=linkedin_url,
            )
        except ValueError as e:
            logger.error(f"Erreur métier lors de la création du profil : {e}")
            return None

        if self.profile_dao.creer_profil(profile):
            logger.info(f"Profil créé pour utilisateur {id_utilisateur}")
            return profile

        logger.error("Échec création profil en base de données")
        return None

    def obtenir_profil_utilisateur(
        self, id_utilisateur: int
    ) -> Optional[CandidateProfile]:
        """Récupère le profil d'un utilisateur"""
        return self.profile_dao.obtenir_profil_par_utilisateur(id_utilisateur)

    def mettre_a_jour_profil(
        self,
        id_utilisateur: int,
        titre_professionnel: Optional[str] = None,
        annees_experience: Optional[int] = None,
        date_disponibilite: Optional[date] = None,
        type_contrat_recherche: Optional[str] = None,
        salaire_min_souhaite: Optional[int] = None,
        cv_path: Optional[str] = None,
        linkedin_url: Optional[str] = None,
    ) -> bool:
        """
        Met à jour le profil d'un utilisateur.
        """

        profile = self.profile_dao.obtenir_profil_par_utilisateur(id_utilisateur)

        if not profile:
            logger.error(f"Profil introuvable pour utilisateur {id_utilisateur}")
            return False

        try:
            if titre_professionnel is not None:
                profile.titre_professionnel = titre_professionnel

            if annees_experience is not None:
                profile.annees_experience = annees_experience

            if date_disponibilite is not None:
                profile.date_disponibilite = date_disponibilite

            if type_contrat_recherche is not None:
                profile.type_contrat_recherche = type_contrat_recherche

            if salaire_min_souhaite is not None:
                profile.salaire_min_souhaite = salaire_min_souhaite

            if cv_path is not None:
                profile.cv_path = cv_path

            if linkedin_url is not None:
                profile.linkedin_url = linkedin_url

            profile._valider_donnees_metier()

        except ValueError as e:
            logger.error(f"Erreur métier lors de la mise à jour : {e}")
            return False

        return self.profile_dao.mettre_a_jour_profil(profile)

    def ajouter_competence(
        self, id_profil: int, nom_competence: str, niveau: str, categorie: str
    ) -> bool:
        if self.skill_dao.competence_existe(id_profil, nom_competence):
            logger.warning(f"Compétence '{nom_competence}' déjà présente")
            return False

        skill = UserSkill(
            id_profil=id_profil,
            nom_competence=nom_competence,
            niveau=niveau,
            categorie=categorie,
        )

        if not skill.valider_niveau():
            logger.error(f"Niveau invalide: {niveau}")
            return False

        return self.skill_dao.ajouter_competence(skill)

    def lister_competences(self, id_profil: int) -> List[UserSkill]:
        return self.skill_dao.lister_competences_utilisateur(id_profil)

    def supprimer_competence(self, id_user_skill: int) -> bool:
        return self.skill_dao.supprimer_competence(id_user_skill)
