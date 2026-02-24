"""DTO pour les compétences"""

from pydantic import BaseModel, Field
from typing import Optional


class SkillDTO(BaseModel):
    """Compétence complète"""

    id_user_skill: int
    id_profil: int
    nom_competence: str
    niveau: str
    categorie: str


class SkillCreateRequest(BaseModel):
    """Créer une compétence"""

    nom_competence: str = Field(..., min_length=1, max_length=100)
    niveau: str = Field(..., pattern="^(Debutant|Intermediaire|Avance|Expert)$")
    categorie: str = Field(..., pattern="^(Langage|Framework|Outil|Soft Skill|Autre)$")


class SkillUpdateRequest(BaseModel):
    """Modifier une compétence"""

    niveau: Optional[str] = Field(
        None, pattern="^(Debutant|Intermediaire|Avance|Expert)$"
    )
    categorie: Optional[str] = Field(
        None, pattern="^(Langage|Framework|Outil|Soft Skill|Autre)$"
    )


class SkillListResponse(BaseModel):
    """Liste des compétences"""

    id_utilisateur: int
    nombre_competences: int
    competences: list[SkillDTO]


class SkillStatsResponse(BaseModel):
    """Statistiques"""

    id_utilisateur: int
    total_competences: int
    par_categorie: dict[str, int]
    par_niveau: dict[str, int]
