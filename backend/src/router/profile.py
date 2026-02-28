from fastapi import APIRouter, Depends, HTTPException
from src.auth.auth_handler import get_utilisateur_from_token
from src.auth.auth_bearer import JWTBearer
from src.services.profile_service import ProfileService
from src.dto.profile_dto import (
    ProfileDTO,
    ProfileUpdateRequest,
    ProfileUpdateResponse,
    ProfileCompletionResponse,
)

router = APIRouter(prefix="/api/profiles", tags=["Profiles"])
profile_service = ProfileService()


@router.get("/me", response_model=ProfileDTO)
def obtenir_profil(token: str = Depends(JWTBearer())):
    id_utilisateur = get_utilisateur_from_token(token).id_utilisateur
    profile = profile_service.obtenir_profil_utilisateur(id_utilisateur)
    print("Utilisateur:", get_utilisateur_from_token(token))  # ← vérifie l'utilisateur
    print("id_utilisateur:", get_utilisateur_from_token(token).id_utilisateur)
    if not profile:
        raise HTTPException(status_code=404, detail="Profil introuvable")

    return ProfileDTO(**profile.to_dict())


@router.put("/update", response_model=ProfileUpdateResponse)
def mettre_a_jour_profil(
    token: str = Depends(JWTBearer()), data: ProfileUpdateRequest = None
):
    id_utilisateur = get_utilisateur_from_token(token).id_utilisateur
    print("id_utilisateur:", id_utilisateur)  # ← vérifie l'id
    print("Données reçues pour mise à jour:", data)  # ← vérifie les données reçues
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="Aucune donnée")

    success = profile_service.mettre_a_jour_profil(id_utilisateur, **update_data)
    if not success:
        raise HTTPException(status_code=404, detail="Profil introuvable")

    return ProfileUpdateResponse(
        message="Profil mis à jour", champs_modifies=list(update_data.keys())
    )


@router.get("/completion", response_model=ProfileCompletionResponse)
def obtenir_taux_completion(token: str = Depends(JWTBearer())):
    id_utilisateur = get_utilisateur_from_token(token).id_utilisateur
    taux = profile_service.calculer_taux_completion_profil(id_utilisateur)
    if taux is None:
        raise HTTPException(status_code=404, detail="Profil introuvable")

    return ProfileCompletionResponse(
        id_utilisateur=id_utilisateur,
        taux_completion=taux,
        message=f"Profil complété à {taux}%",
    )
