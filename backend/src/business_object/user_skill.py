from typing import Optional


class UserSkill:
    """
    Classe métier représentant une compétence déclarée par un candidat.

    Attributs
    ----------
    id_user_skill : Optional[int]
        Identifiant unique de la compétence .
    id_profil : int
        Identifiant du profil candidat auquel appartient la compétence.
    nom_competence : str
        Nom de la compétence ,
    niveau : str
        Niveau de maîtrise de la compétence.
    categorie : str
        Catégorie de la compétence.
    """

    NIVEAUX_VALIDES = ["Debutant", "Intermediaire", "Avance", "Expert"]
    CATEGORIES_VALIDES = ["Langage", "Framework", "Outil", "Soft Skill", "Autre"]

    def __init__(
        self,
        id_profil: int,
        nom_competence: str,
        niveau: str,
        categorie: str,
        id_user_skill: Optional[int] = None,
    ):
        self.id_user_skill = id_user_skill
        self.id_profil = id_profil
        self.nom_competence = nom_competence
        self.niveau = niveau
        self.categorie = categorie

        self._valider_niveau()
        self._valider_categorie()

    def _valider_niveau(self):
        if self.niveau not in self.NIVEAUX_VALIDES:
            raise ValueError(f"Niveau invalide : {self.niveau}")

    def _valider_categorie(self):
        if self.categorie not in self.CATEGORIES_VALIDES:
            raise ValueError(f"Catégorie invalide : {self.categorie}")
