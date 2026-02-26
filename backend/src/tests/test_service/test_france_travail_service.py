"""Tests unitaires pour FranceTravailService"""

from datetime import datetime
from unittest.mock import MagicMock, patch, Mock

from src.services.france_travail_service import FranceTravailService
from src.business_object.job_offer import JobOffer


DATE_TEST = datetime(2026, 2, 19, 16, 50, 45)

offre_json_test = {
    "id": "204GHCG",
    "intitule": "Data Scientist (H/F)",
    "dateCreation": "2026-02-19T16:50:45.422Z",
    "dateActualisation": "2026-02-19T16:50:45.422Z",
    "entreprise": {"nom": "SKARLETT ASSURANCES"},
    "typeContrat": "CDI",
    "typeContratLibelle": "CDI",
    "salaire": {"libelle": "Annuel de 40000€ à 50000€"},
    "lieuTravail": {"libelle": "75 - Paris"},
    "description": "Nous recherchons un Data Scientist avec Python et SQL",
    "competences": [
        {"code": "123", "libelle": "Python", "exigence": "E"},
        {"code": "456", "libelle": "SQL", "exigence": "E"},
    ],
    "origineOffre": {
        "origine": "1",
        "urlOrigine": "https://candidat.francetravail.fr/offres/recherche/detail/204GHCG",
    },
}


def test_parse_offre_ok():
    """Parsing offre avec toutes les données"""
    # GIVEN
    service = FranceTravailService()

    # WHEN
    offre = service._parse_offre(offre_json_test)

    # THEN
    assert offre.external_id == "204GHCG"
    assert offre.titre == "Data Scientist (H/F)"
    assert offre.entreprise == "SKARLETT ASSURANCES"
    assert offre.salaire == "Annuel de 40000€ à 50000€"
    assert offre.localisation == "75 - Paris"
    assert offre.type_contrat == "CDI"
    assert "Python" in offre.competences_requises
    assert "SQL" in offre.competences_requises
    assert (
        offre.url_origine
        == "https://candidat.francetravail.fr/offres/recherche/detail/204GHCG"
    )


def test_parse_offre_sans_competences():
    """Parsing offre sans compétences (extraction depuis description)"""
    # GIVEN
    service = FranceTravailService()
    offre_sans_competences = offre_json_test.copy()
    offre_sans_competences["competences"] = []
    offre_sans_competences["description"] = (
        "Nous cherchons quelqu'un avec Python et Docker"
    )

    # WHEN
    offre = service._parse_offre(offre_sans_competences)

    # THEN
    assert "Python" in offre.competences_requises
    assert "Docker" in offre.competences_requises


def test_parse_offre_sans_salaire():
    """Parsing offre sans salaire"""
    # GIVEN
    service = FranceTravailService()
    offre_sans_salaire = offre_json_test.copy()
    offre_sans_salaire["salaire"] = {}

    # WHEN
    offre = service._parse_offre(offre_sans_salaire)

    # THEN
    assert offre.salaire == "Non renseigné"


def test_parse_offre_sans_url():
    """Parsing offre sans URL"""
    # GIVEN
    service = FranceTravailService()
    offre_sans_url = offre_json_test.copy()
    offre_sans_url["origineOffre"] = {}

    # WHEN
    offre = service._parse_offre(offre_sans_url)

    # THEN
    assert offre.url_origine is None


def test_parse_offre_entreprise_manquante():
    """Parsing offre sans entreprise"""
    # GIVEN
    service = FranceTravailService()
    offre_sans_entreprise = offre_json_test.copy()
    offre_sans_entreprise["entreprise"] = {}

    # WHEN
    offre = service._parse_offre(offre_sans_entreprise)

    # THEN
    assert offre.entreprise == "Non renseigné"


def test_parse_date_ok():
    """Parsing date ISO 8601 valide"""
    # GIVEN
    date_str = "2026-02-19T16:50:45.422Z"

    # WHEN
    date_parsed = FranceTravailService._parse_date(date_str)

    # THEN
    assert date_parsed is not None
    assert isinstance(date_parsed, datetime)
    assert date_parsed.year == 2026
    assert date_parsed.month == 2
    assert date_parsed.day == 19


def test_parse_date_none():
    """Parsing date None retourne datetime.now()"""
    # GIVEN
    date_str = None

    # WHEN
    date_parsed = FranceTravailService._parse_date(date_str)

    # THEN
    assert date_parsed is not None
    assert isinstance(date_parsed, datetime)


def test_parse_date_invalide():
    """Parsing date invalide retourne datetime.now()"""
    # GIVEN
    date_str = "date_invalide"

    # WHEN
    date_parsed = FranceTravailService._parse_date(date_str)

    # THEN
    assert date_parsed is not None
    assert isinstance(date_parsed, datetime)


def test_obtenir_token_ok():
    """Obtention token OAuth2 réussie"""
    # GIVEN
    mock_response = Mock()
    mock_response.json.return_value = {"access_token": "token_123"}
    mock_response.raise_for_status = Mock()

    service = FranceTravailService()
    service.client_id = "test_id"
    service.client_secret = "test_secret"

    # WHEN
    with patch("requests.post", return_value=mock_response):
        token = service._obtenir_token()

    # THEN
    assert token == "token_123"
    assert service.token == "token_123"


def test_obtenir_token_cache():
    """Token déjà en cache"""
    # GIVEN
    service = FranceTravailService()
    service.token = "cached_token"

    # WHEN
    with patch("requests.post") as mock_post:
        token = service._obtenir_token()

    # THEN
    assert token == "cached_token"
    mock_post.assert_not_called()


def test_obtenir_token_echec():
    """Obtention token échouée"""
    # GIVEN
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("Auth error")

    service = FranceTravailService()
    service.client_id = "test_id"
    service.client_secret = "test_secret"

    # WHEN
    with patch("requests.post", return_value=mock_response):
        token = service._obtenir_token()

    # THEN
    assert token is None
    assert service.token is None


def test_rechercher_batch_ok():
    """Recherche batch réussie"""
    # GIVEN
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"resultats": [offre_json_test]}

    service = FranceTravailService()
    service.token = "test_token"

    # WHEN
    with patch("requests.get", return_value=mock_response):
        offres = service._rechercher_batch("data scientist", None, 0, 150)

    # THEN
    assert len(offres) == 1
    assert offres[0].external_id == "204GHCG"


def test_rechercher_batch_status_204():
    """Recherche batch aucun résultat (204)"""
    # GIVEN
    mock_response = Mock()
    mock_response.status_code = 204

    service = FranceTravailService()
    service.token = "test_token"

    # WHEN
    with patch("requests.get", return_value=mock_response):
        offres = service._rechercher_batch("inexistant", None, 0, 150)

    # THEN
    assert offres == []


def test_rechercher_batch_status_416():
    """Recherche batch fin de pagination (416)"""
    # GIVEN
    mock_response = Mock()
    mock_response.status_code = 416

    service = FranceTravailService()
    service.token = "test_token"

    # WHEN
    with patch("requests.get", return_value=mock_response):
        offres = service._rechercher_batch("data", None, 1000, 150)

    # THEN
    assert offres == []


def test_rechercher_batch_sans_token():
    """Recherche batch sans token"""
    # GIVEN
    service = FranceTravailService()
    service._obtenir_token = MagicMock(return_value=None)

    # WHEN
    offres = service._rechercher_batch("data", None, 0, 150)

    # THEN
    assert offres == []


def test_rechercher_batch_avec_departement():
    """Recherche batch avec département"""
    # GIVEN
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"resultats": [offre_json_test]}

    service = FranceTravailService()
    service.token = "test_token"

    # WHEN
    with patch("requests.get", return_value=mock_response) as mock_get:
        offres = service._rechercher_batch("data", "35", 0, 150)

    # THEN
    assert len(offres) == 1
    # Vérifier que le département est passé dans les params
    call_kwargs = mock_get.call_args[1]
    assert call_kwargs["params"]["departement"] == "35"


def test_rechercher_offres_ok():
    """Recherche offres avec résultats"""
    # GIVEN
    service = FranceTravailService()
    service._rechercher_batch = MagicMock(
        return_value=[
            JobOffer(
                external_id="1",
                titre="Test",
                entreprise="Test",
                description="Test",
                localisation="Paris",
                type_contrat="CDI",
                source="france_travail",
            )
        ]
    )

    # WHEN
    with patch("time.sleep"):
        offres = service.rechercher_offres("data", None, 150)

    # THEN
    assert len(offres) == 1


def test_rechercher_offres_arret_si_batch_incomplet():
    """Recherche s'arrête si batch < 150"""
    # GIVEN
    service = FranceTravailService()

    # Premier appel: 80 offres (< 150)
    service._rechercher_batch = MagicMock(
        return_value=[
            JobOffer(
                external_id=str(i),
                titre="Test",
                entreprise="Test",
                description="Test",
                localisation="Paris",
                type_contrat="CDI",
                source="france_travail",
            )
            for i in range(80)
        ]
    )

    # WHEN
    with patch("time.sleep"):
        offres = service.rechercher_offres("data", None, 500)

    # THEN
    assert len(offres) == 80
    # Un seul appel car batch < 150
    service._rechercher_batch.assert_called_once()


def test_rechercher_offres_limite_1000():
    """Recherche s'arrête à la limite 1000"""
    # GIVEN
    service = FranceTravailService()

    # Chaque batch retourne 150 offres
    call_count = [0]

    def mock_batch(*args):
        call_count[0] += 1
        return [
            JobOffer(
                external_id=f"{call_count[0]}_{i}",
                titre="Test",
                entreprise="Test",
                description="Test",
                localisation="Paris",
                type_contrat="CDI",
                source="france_travail",
            )
            for i in range(150)
        ]

    service._rechercher_batch = MagicMock(side_effect=mock_batch)

    # WHEN
    with patch("time.sleep"):
        offres = service.rechercher_offres("data", None, 2000)

    # THEN
    # Doit s'arrêter à ~1000 (7 batches max)
    assert len(offres) <= 1050


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
