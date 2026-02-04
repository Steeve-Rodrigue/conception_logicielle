from datetime import date, datetime
from typing import Optional


class CandidateProfile:
    """
    Classe métier représentant le profil d'un candidat.


    Attributs
    ----------
    id_profil : Optional[int]
        Identifiant du profil candidat.
    id_utilisateur : int
        Identifiant de l'utilisateur associé.
    titre_professionnel : str
        Titre professionnel du candidat.
    annees_experience : int
        Nombre d'années d'expérience.
    date_disponibilite : date
        Date à partir de laquelle le candidat est disponible.
    type_contrat_recherche : str
        Type de contrat recherché.
    salaire_min_souhaite : Optional[int]
        Salaire minimum souhaité.
    cv_path : Optional[str]
        Chemin vers le CV.
    linkedin_url : Optional[str]
        URL du profil LinkedIn.
    date_maj : datetime
        Date de dernière mise à jour du profil.
    """

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
        if self.annees_experience < 0:
            raise ValueError("Les années d'expérience ne peuvent pas être négatives.")

        if self.type_contrat_recherche not in self.TYPES_CONTRAT_VALIDES:
            raise ValueError(
                f"Type de contrat invalide : {self.type_contrat_recherche}"
            )

        if self.date_disponibilite < date.today():
            raise ValueError("La date de disponibilité ne peut pas être dans le passé.")
