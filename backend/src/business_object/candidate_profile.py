from datetime import date, datetime
from typing import Optional


class CandidateProfile:
    """Classe métier représentant le profil d'un candidat"""

    TYPES_CONTRAT_VALIDES = ["CDI", "CDD", "Freelance", "Stage", "Alternance"]

    def __init__(
        self,
        id_utilisateur: int,
        titre_professionnel: str,
        annees_experience: int,
        date_disponibilite: date,
        type_contrat_recherche: str,
        salaire_min_souhaite: Optional[int] = None,
        cv_path: Optional[str] = None,
        linkedin_url: Optional[str] = None,
        id_profil: Optional[int] = None,
        date_maj: Optional[datetime] = None,
    ):
        self.id_profil = id_profil
        self.id_utilisateur = id_utilisateur
        self.titre_professionnel = titre_professionnel
        self.annees_experience = annees_experience
        self.date_disponibilite = date_disponibilite
        self.type_contrat_recherche = type_contrat_recherche
        self.salaire_min_souhaite = salaire_min_souhaite
        self.cv_path = cv_path
        self.linkedin_url = linkedin_url
        self.date_maj = date_maj or datetime.now()

        self._valider_donnees_metier()

    def _valider_donnees_metier(self) -> None:
        """Valide les règles métier"""
        if self.annees_experience < 0:
            raise ValueError("Les années d'expérience ne peuvent pas être négatives")

        if self.type_contrat_recherche not in self.TYPES_CONTRAT_VALIDES:
            raise ValueError(
                f"Type de contrat invalide : {self.type_contrat_recherche}"
            )

        if self.date_disponibilite < date.today():
            raise ValueError("La date de disponibilité ne peut pas être dans le passé")

    def to_dict(self) -> dict:
        """Convertit le profil en dictionnaire"""
        return {
            "id_profil": self.id_profil,
            "id_utilisateur": self.id_utilisateur,
            "titre_professionnel": self.titre_professionnel,
            "annees_experience": self.annees_experience,
            "date_disponibilite": (
                self.date_disponibilite.isoformat() if self.date_disponibilite else None
            ),
            "type_contrat_recherche": self.type_contrat_recherche,
            "salaire_min_souhaite": self.salaire_min_souhaite,
            "cv_path": self.cv_path,
            "linkedin_url": self.linkedin_url,
            "date_maj": self.date_maj.isoformat() if self.date_maj else None,
            "taux_completion": self.calculer_taux_completion(),
        }

    def calculer_taux_completion(self) -> float:
        """Calcule le taux de complétion du profil (0-100%)"""
        total = 0.0

        # Champs obligatoires (60%)
        total += 70.0

        # Champs optionnels (10% chacun)
        if self.salaire_min_souhaite is not None:
            total += 10.0

        if self.cv_path:
            total += 10.0

        if self.linkedin_url:
            total += 10.0

        return total
