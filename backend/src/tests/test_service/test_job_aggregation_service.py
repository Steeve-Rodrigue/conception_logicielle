"""Tests unitaires pour JobAggregationService"""

from unittest.mock import MagicMock
from typing import List

from src.services.job_aggregation_service import JobAggregationService
from src.business_object.job_offer import JobOffer



def creer_offre_test(external_id: str, titre: str) -> JobOffer:
    """Crée une offre de test"""
    return JobOffer(
        external_id=external_id,
        titre=titre,
        entreprise="Test Entreprise",
        description="Description test",
        localisation="Paris",
        type_contrat="CDI",
        source="france_travail"
    )



def test_synchroniser_offres_ok():
    """Synchronisation réussie avec plusieurs termes"""
    # GIVEN
    service = JobAggregationService()
    
    # Mock France Travail - retourner des offres DIFFÉRENTES pour chaque terme
    call_count = [0]
    def mock_recherche(*args, **kwargs):
        call_count[0] += 1
        return [
            creer_offre_test(f"{call_count[0]}_1", "Data Scientist"),
            creer_offre_test(f"{call_count[0]}_2", "ML Engineer")
        ]
    
    service.france_travail.rechercher_offres = MagicMock(side_effect=mock_recherche)
    service.job_offer_dao.creer_offre = MagicMock(return_value=True)

    # WHEN
    count = service.synchroniser_offres(["data scientist", "machine learning"])

    # THEN
    assert count == 4  # 2 offres × 2 termes = 4 offres


def test_synchroniser_offres_avec_doublons():
    """Synchronisation avec déduplication entre termes"""
    # GIVEN
    service = JobAggregationService()
    
    #même offre retournée pour les 2 termes
    service.france_travail.rechercher_offres = MagicMock(return_value=[
        creer_offre_test("123", "Data Scientist"),
        creer_offre_test("456", "ML Engineer")
    ])
    
    service.job_offer_dao.creer_offre = MagicMock(return_value=True)

    # WHEN
    count = service.synchroniser_offres(["data", "data scientist"])

    # THEN
    assert count == 2  
    assert service.job_offer_dao.creer_offre.call_count == 2


def test_synchroniser_offres_aucun_resultat():
    """Synchronisation sans résultats"""
    # GIVEN
    service = JobAggregationService()
    service.france_travail.rechercher_offres = MagicMock(return_value=[])

    # WHEN
    count = service.synchroniser_offres(["inexistant"])

    # THEN
    assert count == 0


def test_synchroniser_offres_echec_dao():
    """Synchronisation avec échec DAO"""
    # GIVEN
    service = JobAggregationService()
    
    service.france_travail.rechercher_offres = MagicMock(return_value=[
        creer_offre_test("1", "Test")
    ])
    
    service.job_offer_dao.creer_offre = MagicMock(return_value=False)

    # WHEN
    count = service.synchroniser_offres(["data"])

    # THEN
    assert count == 0


def test_synchroniser_offres_avec_departement():
    """Synchronisation avec département"""
    # GIVEN
    service = JobAggregationService()
    
    service.france_travail.rechercher_offres = MagicMock(return_value=[
        creer_offre_test("1", "Test")
    ])
    
    service.job_offer_dao.creer_offre = MagicMock(return_value=True)

    # WHEN
    count = service.synchroniser_offres(["data"], departement="35")

    # THEN
    assert count == 1
    service.france_travail.rechercher_offres.assert_called_with(
        mots_cles="data",
        departement="35"
    )


def test_synchroniser_offres_liste_vide():
    """Synchronisation avec liste de termes vide"""
    # GIVEN
    service = JobAggregationService()

    # WHEN
    count = service.synchroniser_offres([])

    # THEN
    assert count == 0


def test_synchroniser_offres_plusieurs_termes():
    """Synchronisation avec 3 termes différents"""
    # GIVEN
    service = JobAggregationService()
    
    call_count = [0]
    def mock_recherche(*args, **kwargs):
        call_count[0] += 1
        return [
            creer_offre_test(f"{call_count[0]}_1", "Offre 1"),
            creer_offre_test(f"{call_count[0]}_2", "Offre 2")
        ]
    
    service.france_travail.rechercher_offres = MagicMock(side_effect=mock_recherche)
    service.job_offer_dao.creer_offre = MagicMock(return_value=True)

    # WHEN
    count = service.synchroniser_offres(["data", "ML", "IA"])

    # THEN
    assert count == 6  # 2 offres × 3 termes
    assert service.france_travail.rechercher_offres.call_count == 3


def test_rechercher_offres_locales_ok():
    """Recherche locale réussie"""
    # GIVEN
    service = JobAggregationService()
    
    offres_mock = [
        creer_offre_test("1", "Data Scientist"),
        creer_offre_test("2", "ML Engineer")
    ]
    
    service.job_offer_dao.rechercher_offres = MagicMock(return_value=offres_mock)

    # WHEN
    offres = service.rechercher_offres_locales(mots_cles="data")

    # THEN
    assert len(offres) == 2
    assert offres[0].titre == "Data Scientist"


def test_rechercher_offres_locales_aucun_resultat():
    """Recherche locale sans résultats"""
    # GIVEN
    service = JobAggregationService()
    service.job_offer_dao.rechercher_offres = MagicMock(return_value=[])

    # WHEN
    offres = service.rechercher_offres_locales(mots_cles="inexistant")

    # THEN
    assert offres == []


def test_rechercher_offres_locales_tous_parametres():
    """Recherche locale avec tous les paramètres"""
    # GIVEN
    service = JobAggregationService()
    service.job_offer_dao.rechercher_offres = MagicMock(return_value=[])

    # WHEN
    service.rechercher_offres_locales(
        mots_cles="data",
        localisation="Paris",
        type_contrat="CDI",
        competences=["Python", "SQL"],
        limit=50,
        offset=10
    )

    # THEN
    service.job_offer_dao.rechercher_offres.assert_called_once_with(
        mots_cles="data",
        localisation="Paris",
        type_contrat="CDI",
        competences=["Python", "SQL"],
        limit=50,
        offset=10
    )


def test_rechercher_offres_locales_sans_parametres():
    """Recherche locale sans paramètres (toutes les offres)"""
    # GIVEN
    service = JobAggregationService()
    
    offres_mock = [creer_offre_test(str(i), f"Offre {i}") for i in range(100)]
    service.job_offer_dao.rechercher_offres = MagicMock(return_value=offres_mock)

    # WHEN
    offres = service.rechercher_offres_locales()

    # THEN
    assert len(offres) == 100


def test_rechercher_offres_locales_avec_localisation():
    """Recherche locale filtrée par localisation"""
    # GIVEN
    service = JobAggregationService()
    service.job_offer_dao.rechercher_offres = MagicMock(return_value=[
        creer_offre_test("1", "Offre Paris")
    ])

    # WHEN
    offres = service.rechercher_offres_locales(localisation="Paris")

    # THEN
    assert len(offres) == 1
    service.job_offer_dao.rechercher_offres.assert_called_once()


def test_rechercher_offres_locales_avec_type_contrat():
    """Recherche locale filtrée par type de contrat"""
    # GIVEN
    service = JobAggregationService()
    service.job_offer_dao.rechercher_offres = MagicMock(return_value=[
        creer_offre_test("1", "CDI Offre")
    ])

    # WHEN
    offres = service.rechercher_offres_locales(type_contrat="CDI")

    # THEN
    assert len(offres) == 1


def test_rechercher_offres_locales_avec_competences():
    """Recherche locale filtrée par compétences"""
    # GIVEN
    service = JobAggregationService()
    service.job_offer_dao.rechercher_offres = MagicMock(return_value=[
        creer_offre_test("1", "Python Developer")
    ])

    # WHEN
    offres = service.rechercher_offres_locales(competences=["Python"])

    # THEN
    assert len(offres) == 1


def test_rechercher_offres_locales_limit_offset():
    """Recherche locale avec pagination"""
    # GIVEN
    service = JobAggregationService()
    
    offres_mock = [creer_offre_test(str(i), f"Offre {i}") for i in range(20)]
    service.job_offer_dao.rechercher_offres = MagicMock(return_value=offres_mock)

    # WHEN
    offres = service.rechercher_offres_locales(limit=20, offset=0)

    # THEN
    assert len(offres) == 20
    service.job_offer_dao.rechercher_offres.assert_called_with(
        mots_cles=None,
        localisation=None,
        type_contrat=None,
        competences=None,
        limit=20,
        offset=0
    )


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])