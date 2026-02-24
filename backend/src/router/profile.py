from fastapi import APIRouter, HTTPException
from src.services.profile_service import ProfileService
from src.dto.profile_dto import (
    ProfileDTO,
    ProfileUpdateRequest,
    ProfileUpdateResponse,
    ProfileCompletionResponse,
)

router = APIRouter(prefix="/api/profiles", tags=["Profiles"])
profile_service = ProfileService()


@router.get("/{id_utilisateur}", response_model=ProfileDTO)
def obtenir_profil(id_utilisateur: int):
    profile = profile_service.obtenir_profil_utilisateur(id_utilisateur)
    if not profile:
        raise HTTPException(status_code=404, detail="Profil introuvable")

    return ProfileDTO(**profile.to_dict())


@router.put("/{id_utilisateur}", response_model=ProfileUpdateResponse)
def mettre_a_jour_profil(id_utilisateur: int, data: ProfileUpdateRequest):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="Aucune donnée")

    success = profile_service.mettre_a_jour_profil(id_utilisateur, **update_data)
    if not success:
        raise HTTPException(status_code=404, detail="Profil introuvable")

    return ProfileUpdateResponse(
        message="Profil mis à jour", champs_modifies=list(update_data.keys())
    )


@router.get("/{id_utilisateur}/completion", response_model=ProfileCompletionResponse)
def obtenir_taux_completion(id_utilisateur: int):
    taux = profile_service.calculer_taux_completion_profil(id_utilisateur)
    if taux is None:
        raise HTTPException(status_code=404, detail="Profil introuvable")

    return ProfileCompletionResponse(
        id_utilisateur=id_utilisateur,
        taux_completion=taux,
        message=f"Profil complété à {taux}%",
    )
