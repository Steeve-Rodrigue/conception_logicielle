"""Tests pour ProfileService"""

from datetime import date, timedelta
from unittest.mock import MagicMock

from src.business_object.candidate_profile import CandidateProfile
from src.business_object.user_skill import UserSkill
from src.services.profile_service import ProfileService

DATE_TEST = date(2026, 3, 1)
DATE_DISPONIBILITE = date(2026, 5, 1)

liste_profils = [
    CandidateProfile(
        id_profil=1,
        id_utilisateur=1,
        titre_professionnel="Data Scientist",
        annees_experience=3,
        date_disponibilite=DATE_DISPONIBILITE,
        type_contrat_recherche="CDI",
        salaire_min_souhaite=50000,
        cv_path="/cv/user1.pdf",
        linkedin_url="https://linkedin.com/in/user1",
    ),
    CandidateProfile(
        id_profil=2,
        id_utilisateur=2,
        titre_professionnel="Data Analyst",
        annees_experience=2,
        date_disponibilite=DATE_DISPONIBILITE,
        type_contrat_recherche="CDD",
        salaire_min_souhaite=40000,
    ),
]

liste_competences = [
    UserSkill(
        id_user_skill=1,
        id_profil=1,
        nom_competence="Python",
        niveau="Avance",
        categorie="Langage",
    ),
    UserSkill(
        id_user_skill=2,
        id_profil=1,
        nom_competence="SQL",
        niveau="Intermediaire",
        categorie="Langage",
    ),
]


def test_creer_profil_ok():
    """Création de profil réussie"""
    # GIVEN
    id_utilisateur = 1
    titre = "Data Scientist"
    experience = 3
    disponibilite = DATE_DISPONIBILITE
    contrat = "CDI"

    service = ProfileService()
    service.profile_dao.creer_profil = MagicMock(return_value=True)

    # WHEN
    profile = service.creer_profil(
        id_utilisateur=id_utilisateur,
        titre_professionnel=titre,
        annees_experience=experience,
        date_disponibilite=disponibilite,
        type_contrat_recherche=contrat,
        salaire_min_souhaite=50000,
    )

    # THEN
    assert profile is not None
    assert profile.titre_professionnel == titre
    assert profile.annees_experience == experience
    assert profile.type_contrat_recherche == contrat


def test_creer_profil_echec_dao():
    """Création de profil échouée (DAO)"""
    # GIVEN
    service = ProfileService()
    service.profile_dao.creer_profil = MagicMock(return_value=False)

    # WHEN
    profile = service.creer_profil(
        id_utilisateur=1,
        titre_professionnel="Data Scientist",
        annees_experience=3,
        date_disponibilite=DATE_DISPONIBILITE,
        type_contrat_recherche="CDI",
    )

    # THEN
    assert profile is None


def test_creer_profil_experience_negative():
    """Création avec expérience négative"""
    # GIVEN
    service = ProfileService()

    # WHEN
    profile = service.creer_profil(
        id_utilisateur=1,
        titre_professionnel="Data Scientist",
        annees_experience=-1,
        date_disponibilite=DATE_DISPONIBILITE,
        type_contrat_recherche="CDI",
    )

    # THEN
    assert profile is None


def test_creer_profil_contrat_invalide():
    """Création avec type de contrat invalide"""
    # GIVEN
    service = ProfileService()

    # WHEN
    profile = service.creer_profil(
        id_utilisateur=1,
        titre_professionnel="Data Scientist",
        annees_experience=3,
        date_disponibilite=DATE_DISPONIBILITE,
        type_contrat_recherche="INVALIDE",
    )

    # THEN
    assert profile is None


def test_creer_profil_date_passee():
    """Création avec date de disponibilité dans le passé"""
    # GIVEN
    service = ProfileService()
    date_passee = date.today() - timedelta(days=1)

    # WHEN
    profile = service.creer_profil(
        id_utilisateur=1,
        titre_professionnel="Data Scientist",
        annees_experience=3,
        date_disponibilite=date_passee,
        type_contrat_recherche="CDI",
    )

    # THEN
    assert profile is None


def test_obtenir_profil_utilisateur_ok():
    """Récupération profil réussie"""
    # GIVEN
    id_utilisateur = 1

    service = ProfileService()
    service.profile_dao.obtenir_profil_par_utilisateur = MagicMock(
        return_value=liste_profils[0]
    )

    # WHEN
    profile = service.obtenir_profil_utilisateur(id_utilisateur)

    # THEN
    assert profile is not None
    assert profile.id_utilisateur == id_utilisateur


def test_obtenir_profil_utilisateur_inexistant():
    """Récupération profil inexistant"""
    # GIVEN
    id_utilisateur = 999

    service = ProfileService()
    service.profile_dao.obtenir_profil_par_utilisateur = MagicMock(return_value=None)

    # WHEN
    profile = service.obtenir_profil_utilisateur(id_utilisateur)

    # THEN
    assert profile is None


def test_mettre_a_jour_profil_ok():
    """Mise à jour profil réussie"""
    # GIVEN
    id_utilisateur = 1
    nouveau_titre = "Senior Data Scientist"

    service = ProfileService()
    service.profile_dao.obtenir_profil_par_utilisateur = MagicMock(
        return_value=liste_profils[0]
    )
    service.profile_dao.mettre_a_jour_profil = MagicMock(return_value=True)

    # WHEN
    result = service.mettre_a_jour_profil(
        id_utilisateur=id_utilisateur,
        titre_professionnel=nouveau_titre,
    )

    # THEN
    assert result is True


def test_mettre_a_jour_profil_inexistant():
    """Mise à jour profil inexistant"""
    # GIVEN
    id_utilisateur = 999

    service = ProfileService()
    service.profile_dao.obtenir_profil_par_utilisateur = MagicMock(return_value=None)

    # WHEN
    result = service.mettre_a_jour_profil(
        id_utilisateur=id_utilisateur,
        titre_professionnel="Nouveau Titre",
    )

    # THEN
    assert result is False


def test_mettre_a_jour_profil_experience_negative():
    """Mise à jour avec expérience négative"""
    # GIVEN
    id_utilisateur = 1

    service = ProfileService()
    service.profile_dao.obtenir_profil_par_utilisateur = MagicMock(
        return_value=liste_profils[0]
    )

    # WHEN
    result = service.mettre_a_jour_profil(
        id_utilisateur=id_utilisateur,
        annees_experience=-1,
    )

    # THEN
    assert result is False


def test_mettre_a_jour_profil_echec_dao():
    """Mise à jour échouée au niveau DAO"""
    # GIVEN
    id_utilisateur = 1

    service = ProfileService()
    service.profile_dao.obtenir_profil_par_utilisateur = MagicMock(
        return_value=liste_profils[0]
    )
    service.profile_dao.mettre_a_jour_profil = MagicMock(return_value=False)

    # WHEN
    result = service.mettre_a_jour_profil(
        id_utilisateur=id_utilisateur,
        titre_professionnel="Nouveau Titre",
    )

    # THEN
    assert result is False


def test_ajouter_competence_ok():
    """Ajout de compétence réussi"""
    # GIVEN
    id_profil = 1
    nom = "Python"
    niveau = "Avance"
    categorie = "Langage"

    service = ProfileService()
    service.skill_dao.competence_existe = MagicMock(return_value=False)
    service.skill_dao.ajouter_competence = MagicMock(return_value=True)

    # WHEN
    result = service.ajouter_competence(id_profil, nom, niveau, categorie)

    # THEN
    assert result is True


def test_ajouter_competence_deja_existante():
    """Ajout compétence déjà existante"""
    # GIVEN
    id_profil = 1
    nom = "Python"
    niveau = "Avance"
    categorie = "Langage"

    service = ProfileService()
    service.skill_dao.competence_existe = MagicMock(return_value=True)

    # WHEN
    result = service.ajouter_competence(id_profil, nom, niveau, categorie)

    # THEN
    assert result is False


def test_ajouter_competence_echec_dao():
    """Ajout compétence échoué (DAO)"""
    # GIVEN
    id_profil = 1
    nom = "Python"
    niveau = "Avance"
    categorie = "Langage"

    service = ProfileService()
    service.skill_dao.competence_existe = MagicMock(return_value=False)
    service.skill_dao.ajouter_competence = MagicMock(return_value=False)

    # WHEN
    result = service.ajouter_competence(id_profil, nom, niveau, categorie)

    # THEN
    assert result is False


def test_lister_competences_ok():
    """Liste des compétences"""
    # GIVEN
    id_profil = 1

    service = ProfileService()
    service.skill_dao.lister_competences_utilisateur = MagicMock(
        return_value=liste_competences
    )

    # WHEN
    competences = service.lister_competences(id_profil)

    # THEN
    assert len(competences) == 2
    assert competences[0].nom_competence == "Python"


def test_lister_competences_vide():
    """Liste vide de compétences"""
    # GIVEN
    id_profil = 999

    service = ProfileService()
    service.skill_dao.lister_competences_utilisateur = MagicMock(return_value=[])

    # WHEN
    competences = service.lister_competences(id_profil)

    # THEN
    assert len(competences) == 0


def test_supprimer_competence_ok():
    """Suppression compétence réussie"""
    # GIVEN
    id_user_skill = 1

    service = ProfileService()
    service.skill_dao.supprimer_competence = MagicMock(return_value=True)

    # WHEN
    result = service.supprimer_competence(id_user_skill)

    # THEN
    assert result is True


def test_supprimer_competence_inexistante():
    """Suppression compétence inexistante"""
    # GIVEN
    id_user_skill = 999

    service = ProfileService()
    service.skill_dao.supprimer_competence = MagicMock(return_value=False)

    # WHEN
    result = service.supprimer_competence(id_user_skill)

    # THEN
    assert result is False


def test_calculer_taux_completion_ok():
    """Calcul taux de complétion réussi"""
    # GIVEN
    id_utilisateur = 1

    service = ProfileService()
    service.profile_dao.obtenir_profil_par_utilisateur = MagicMock(
        return_value=liste_profils[0]
    )

    # WHEN
    taux = service.calculer_taux_completion_profil(id_utilisateur)

    # THEN
    assert taux is not None
    assert 0 <= taux <= 100


def test_calculer_taux_completion_profil_inexistant():
    """Calcul taux de complétion profil inexistant"""
    # GIVEN
    id_utilisateur = 999

    service = ProfileService()
    service.profile_dao.obtenir_profil_par_utilisateur = MagicMock(return_value=None)

    # WHEN
    taux = service.calculer_taux_completion_profil(id_utilisateur)

    # THEN
    assert taux is None


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
