from fastapi import APIRouter, HTTPException, Depends
from typing import List
from src.auth.auth_bearer import JWTBearer
from src.auth.auth_handler import get_utilisateur_from_token
from src.services.profile_service import ProfileService
from src.dto.skill_dto import (
    SkillDTO,
    SkillCreateRequest,
    SkillUpdateRequest,
    SkillListResponse,
    SkillStatsResponse,
)

router = APIRouter(prefix="/api/profiles", tags=["Skills"])
profile_service = ProfileService()


@router.post("/skills", status_code=201)
def ajouter_competence(
    token: str = Depends(JWTBearer()), data: SkillCreateRequest = None
):
    id_utilisateur = get_utilisateur_from_token(token).id_utilisateur
    profile = profile_service.obtenir_profil_utilisateur(id_utilisateur)
    if not profile:
        raise HTTPException(status_code=404, detail="Profil introuvable")

    success = profile_service.ajouter_competence(
        id_profil=profile.id_profil,
        nom_competence=data.nom_competence,
        niveau=data.niveau,
        categorie=data.categorie,
    )

    if not success:
        raise HTTPException(status_code=400, detail="Impossible d'ajouter")

    return {"message": f"Compétence '{data.nom_competence}' ajoutée"}


@router.get("/skill_list", response_model=SkillListResponse)
def lister_competences(token: str = Depends(JWTBearer())):
    id_utilisateur = get_utilisateur_from_token(token).id_utilisateur
    profile = profile_service.obtenir_profil_utilisateur(id_utilisateur)
    if not profile:
        raise HTTPException(status_code=404, detail="Profil introuvable")

    skills = profile_service.lister_competences(profile.id_profil)

    return SkillListResponse(
        id_utilisateur=id_utilisateur,
        nombre_competences=len(skills),
        competences=[SkillDTO(**s.__dict__) for s in skills],
    )


@router.put("/skills/{id_user_skill}")
def modifier_competence(id_user_skill: int, data: SkillUpdateRequest):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="Aucune donnée")

    success = profile_service.modifier_competence(id_user_skill, **update_data)
    if not success:
        raise HTTPException(status_code=404, detail="Compétence introuvable")

    return {"message": "Compétence modifiée"}


@router.delete("/skills/{id_user_skill}", status_code=204)
def supprimer_competence(id_user_skill: int):
    success = profile_service.supprimer_competence(id_user_skill)
    if not success:
        raise HTTPException(status_code=404, detail="Compétence introuvable")
    return None


@router.post("/{id_utilisateur}/skills/bulk", status_code=201)
def ajouter_competences_multiples(
    id_utilisateur: int, skills: List[SkillCreateRequest]
):
    profile = profile_service.obtenir_profil_utilisateur(id_utilisateur)
    if not profile:
        raise HTTPException(status_code=404, detail="Profil introuvable")

    ajoutees = 0
    erreurs = []

    for skill in skills:
        success = profile_service.ajouter_competence(
            id_profil=profile.id_profil,
            nom_competence=skill.nom_competence,
            niveau=skill.niveau,
            categorie=skill.categorie,
        )
        if success:
            ajoutees += 1
        else:
            erreurs.append(skill.nom_competence)

    return {
        "message": f"{ajoutees} compétences ajoutées",
        "ajoutees": ajoutees,
        "ignorees": len(erreurs),
    }


@router.get("/{id_utilisateur}/skills/stats", response_model=SkillStatsResponse)
def statistiques_competences(id_utilisateur: int):
    profile = profile_service.obtenir_profil_utilisateur(id_utilisateur)
    if not profile:
        raise HTTPException(status_code=404, detail="Profil introuvable")

    skills = profile_service.lister_competences(profile.id_profil)

    par_categorie = {}
    par_niveau = {}

    for skill in skills:
        par_categorie[skill.categorie] = par_categorie.get(skill.categorie, 0) + 1
        par_niveau[skill.niveau] = par_niveau.get(skill.niveau, 0) + 1

    return SkillStatsResponse(
        id_utilisateur=id_utilisateur,
        total_competences=len(skills),
        par_categorie=par_categorie,
        par_niveau=par_niveau,
    )
