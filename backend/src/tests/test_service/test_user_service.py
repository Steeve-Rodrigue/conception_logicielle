"""Tests pour UserService"""

from datetime import datetime
from unittest.mock import MagicMock, patch

from src.business_object.user import User
from src.services.user_service import UserService
from src.utils.security import hash_password

DATE_TEST = datetime(2026, 1, 1, 12, 0, 0)

liste_utilisateurs = [
    User(
        id_utilisateur=1,
        email="test1@test.com",
        pseudo="user1",
        nom="Test",
        prenom="Un",
        mdp_hash=hash_password("MotDePasse123!"),
        date_creation=DATE_TEST,
        date_derniere_connexion=DATE_TEST,
    ),
    User(
        id_utilisateur=2,
        email="test2@test.com",
        pseudo="user2",
        nom="Test",
        prenom="Deux",
        mdp_hash=hash_password("MotDePasse456!"),
        date_creation=DATE_TEST,
        date_derniere_connexion=DATE_TEST,
    ),
    User(
        id_utilisateur=3,
        email="test3@test.com",
        pseudo="user3",
        nom="Test",
        prenom="Trois",
        mdp_hash=hash_password("MotDePasse789!"),
        date_creation=DATE_TEST,
        date_derniere_connexion=DATE_TEST,
    ),
]


def test_creer_utilisateur_ok():
    """Création d'utilisateur réussie"""
    # GIVEN
    email, pseudo, mdp = "nouveau@test.com", "nouveau", "MotDePasse123!"
    nom, prenom = "Nouveau", "User"

    service = UserService()
    service.user_dao.trouver_par_email = MagicMock(return_value=None)
    service.user_dao.trouver_par_pseudo = MagicMock(return_value=None)
    service.user_dao.creer_compte = MagicMock(return_value=True)
    service.profile_service.creer_profil = MagicMock(return_value=True)

    # WHEN
    user = service.creer_utilisateur(email, pseudo, mdp, nom, prenom)

    # THEN
    assert user is not None
    assert user.email == email
    assert user.pseudo == pseudo
    assert user.date_creation is not None


def test_creer_utilisateur_echec_dao():
    """Création d'utilisateur échouée (DAO)"""
    # GIVEN
    email, pseudo, mdp = "nouveau@test.com", "nouveau", "MotDePasse123!"
    nom, prenom = "Nouveau", "User"

    service = UserService()
    service.user_dao.trouver_par_email = MagicMock(return_value=None)
    service.user_dao.trouver_par_pseudo = MagicMock(return_value=None)
    service.user_dao.creer_compte = MagicMock(return_value=False)

    # WHEN
    user = service.creer_utilisateur(email, pseudo, mdp, nom, prenom)

    # THEN
    assert user is None


def test_creer_utilisateur_email_invalide():
    """Création avec email invalide"""
    # GIVEN
    email, pseudo, mdp = "email_invalide", "nouveau", "MotDePasse123!"
    nom, prenom = "Nouveau", "User"

    service = UserService()

    # WHEN
    user = service.creer_utilisateur(email, pseudo, mdp, nom, prenom)

    # THEN
    assert user is None


def test_creer_utilisateur_mdp_faible():
    """Création avec mot de passe trop faible"""
    # GIVEN
    email, pseudo, mdp = "nouveau@test.com", "nouveau", "123"
    nom, prenom = "Nouveau", "User"

    service = UserService()
    service.user_dao.trouver_par_email = MagicMock(return_value=None)
    service.user_dao.trouver_par_pseudo = MagicMock(return_value=None)

    # WHEN
    user = service.creer_utilisateur(email, pseudo, mdp, nom, prenom)

    # THEN
    assert user is None


def test_creer_utilisateur_email_deja_utilise():
    """Création avec email déjà existant"""
    # GIVEN
    email, pseudo, mdp = "test1@test.com", "nouveau", "MotDePasse123!"
    nom, prenom = "Nouveau", "User"

    service = UserService()
    service.user_dao.trouver_par_email = MagicMock(return_value=liste_utilisateurs[0])

    # WHEN
    user = service.creer_utilisateur(email, pseudo, mdp, nom, prenom)

    # THEN
    assert user is None


def test_creer_utilisateur_pseudo_deja_utilise():
    """Création avec pseudo déjà existant"""
    # GIVEN
    email, pseudo, mdp = "nouveau@test.com", "user1", "MotDePasse123!"
    nom, prenom = "Nouveau", "User"

    service = UserService()
    service.user_dao.trouver_par_email = MagicMock(return_value=None)
    service.user_dao.trouver_par_pseudo = MagicMock(return_value=liste_utilisateurs[0])

    # WHEN
    user = service.creer_utilisateur(email, pseudo, mdp, nom, prenom)

    # THEN
    assert user is None


def test_se_connecter_ok():
    """Connexion réussie"""
    # GIVEN
    email, mdp = "test1@test.com", "MotDePasse123!"

    service = UserService()
    service.user_dao.trouver_par_email = MagicMock(return_value=liste_utilisateurs[0])
    service.user_dao.mettre_a_jour_derniere_connexion = MagicMock(return_value=True)

    # WHEN
    with patch("src.services.user_service.verify_password", return_value=True):
        user = service.se_connecter(email, mdp)

    # THEN
    assert user is not None
    assert user.email == email


def test_se_connecter_email_inexistant():
    """Connexion avec email inexistant"""
    # GIVEN
    email, mdp = "inexistant@test.com", "MotDePasse123!"

    service = UserService()
    service.user_dao.trouver_par_email = MagicMock(return_value=None)

    # WHEN
    user = service.se_connecter(email, mdp)

    # THEN
    assert user is None


def test_se_connecter_mdp_incorrect():
    """Connexion avec mot de passe incorrect"""
    # GIVEN
    email, mdp = "test1@test.com", "MauvaisMotDePasse"

    service = UserService()
    service.user_dao.trouver_par_email = MagicMock(return_value=liste_utilisateurs[0])

    # WHEN
    with patch("src.services.user_service.verify_password", return_value=False):
        user = service.se_connecter(email, mdp)

    # THEN
    assert user is None


def test_modifier_utilisateur_ok():
    """Modification utilisateur réussie"""
    # GIVEN
    id_utilisateur = 1
    nouveau_nom = "Nouveau Nom"

    service = UserService()
    service.user_dao.trouver_par_id = MagicMock(return_value=liste_utilisateurs[0])
    service.user_dao.modifier = MagicMock(return_value=True)

    # WHEN
    result = service.modifier_utilisateur(id_utilisateur, nom=nouveau_nom)

    # THEN
    assert result is True


def test_modifier_utilisateur_inexistant():
    """Modification utilisateur inexistant"""
    # GIVEN
    id_utilisateur = 999

    service = UserService()
    service.user_dao.trouver_par_id = MagicMock(return_value=None)

    # WHEN
    result = service.modifier_utilisateur(id_utilisateur, nom="Test")

    # THEN
    assert result is False


def test_modifier_utilisateur_email_deja_utilise():
    """Modification avec email déjà utilisé"""
    # GIVEN
    id_utilisateur = 1
    email_existant = "test2@test.com"

    service = UserService()
    service.user_dao.trouver_par_id = MagicMock(return_value=liste_utilisateurs[0])
    service.user_dao.trouver_par_email = MagicMock(return_value=liste_utilisateurs[1])

    # WHEN
    result = service.modifier_utilisateur(id_utilisateur, email=email_existant)

    # THEN
    assert result is False


def test_modifier_utilisateur_pseudo_deja_utilise():
    """Modification avec pseudo déjà utilisé"""
    # GIVEN
    id_utilisateur = 1
    pseudo_existant = "user2"

    service = UserService()
    service.user_dao.trouver_par_id = MagicMock(return_value=liste_utilisateurs[0])
    service.user_dao.trouver_par_pseudo = MagicMock(return_value=liste_utilisateurs[1])

    # WHEN
    result = service.modifier_utilisateur(id_utilisateur, pseudo=pseudo_existant)

    # THEN
    assert result is False


def test_changer_mot_de_passe_ok():
    """Changement de mot de passe réussi"""
    # GIVEN
    id_utilisateur = 1
    ancien_mdp, nouveau_mdp = "MotDePasse123!", "NouveauMotDePasse123!"

    service = UserService()
    service.user_dao.trouver_par_id = MagicMock(return_value=liste_utilisateurs[0])
    service.user_dao.modifier = MagicMock(return_value=True)

    # WHEN
    with patch("src.services.user_service.verify_password", return_value=True):
        result = service.changer_mot_de_passe(id_utilisateur, ancien_mdp, nouveau_mdp)

    # THEN
    assert result is True


def test_changer_mot_de_passe_ancien_incorrect():
    """Changement avec ancien mot de passe incorrect"""
    # GIVEN
    id_utilisateur = 1
    ancien_mdp, nouveau_mdp = "MauvaisMotDePasse", "NouveauMotDePasse123!"

    service = UserService()
    service.user_dao.trouver_par_id = MagicMock(return_value=liste_utilisateurs[0])

    # WHEN
    with patch("src.services.user_service.verify_password", return_value=False):
        result = service.changer_mot_de_passe(id_utilisateur, ancien_mdp, nouveau_mdp)

    # THEN
    assert result is False


def test_changer_mot_de_passe_nouveau_faible():
    """Changement avec nouveau mot de passe faible"""
    # GIVEN
    id_utilisateur = 1
    ancien_mdp, nouveau_mdp = "MotDePasse123!", "123"

    service = UserService()
    service.user_dao.trouver_par_id = MagicMock(return_value=liste_utilisateurs[0])

    # WHEN
    with patch("src.services.user_service.verify_password", return_value=True):
        result = service.changer_mot_de_passe(id_utilisateur, ancien_mdp, nouveau_mdp)

    # THEN
    assert result is False


def test_changer_mot_de_passe_echec_dao():
    """Changement échoué au niveau DAO"""
    # GIVEN
    id_utilisateur = 1
    ancien_mdp, nouveau_mdp = "MotDePasse123!", "NouveauMotDePasse123!"

    service = UserService()
    service.user_dao.trouver_par_id = MagicMock(return_value=liste_utilisateurs[0])
    service.user_dao.modifier = MagicMock(return_value=False)

    # WHEN
    with patch("src.services.user_service.verify_password", return_value=True):
        result = service.changer_mot_de_passe(id_utilisateur, ancien_mdp, nouveau_mdp)

    # THEN
    assert result is False


def test_supprimer_utilisateur_ok():
    """Suppression utilisateur réussie"""
    # GIVEN
    id_utilisateur = 1

    service = UserService()
    service.user_dao.supprimer = MagicMock(return_value=True)

    # WHEN
    result = service.supprimer_utilisateur(id_utilisateur)

    # THEN
    assert result is True


def test_supprimer_utilisateur_echec():
    """Suppression utilisateur échouée"""
    # GIVEN
    id_utilisateur = 999

    service = UserService()
    service.user_dao.supprimer = MagicMock(return_value=False)

    # WHEN
    result = service.supprimer_utilisateur(id_utilisateur)

    # THEN
    assert result is False


def test_email_deja_utilise_oui():
    """Email déjà utilisé"""
    # GIVEN
    email = "test1@test.com"

    service = UserService()
    service.user_dao.trouver_par_email = MagicMock(return_value=liste_utilisateurs[0])

    # WHEN
    result = service.email_deja_utilise(email)

    # THEN
    assert result is True


def test_email_deja_utilise_non():
    """Email disponible"""
    # GIVEN
    email = "disponible@test.com"

    service = UserService()
    service.user_dao.trouver_par_email = MagicMock(return_value=None)

    # WHEN
    result = service.email_deja_utilise(email)

    # THEN
    assert result is False


def test_pseudo_deja_utilise_oui():
    """Pseudo déjà utilisé"""
    # GIVEN
    pseudo = "user1"

    service = UserService()
    service.user_dao.trouver_par_pseudo = MagicMock(return_value=liste_utilisateurs[0])

    # WHEN
    result = service.pseudo_deja_utilise(pseudo)

    # THEN
    assert result is True
