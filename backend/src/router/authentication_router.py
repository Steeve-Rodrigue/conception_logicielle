"""
Routes d'authentification de l'API.

Expose les endpoints pour la connexion, l'inscription,
la déconnexion et la récupération des informations utilisateur.
Utilise JWT pour la gestion des tokens d'authentification.
"""

from fastapi import APIRouter, HTTPException, Depends, status

from src.auth.auth_handler import (
    check_utilisateur,
    sign_jwt,
    get_utilisateur_from_token,
)
from src.auth.auth_bearer import JWTBearer
from src.services.user_service import UserService
from src.authentication_dto import (
    LoginRequest,
    SignupRequest,
    LoginResponse,
    UtilisateurResponse,
    MessageResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentification"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Connexion utilisateur",
    description="Authentifie un utilisateur et retourne un token JWT",
)
async def login(credentials: LoginRequest):
    try:
        utilisateur_id = check_utilisateur(
            email=credentials.email, mdp=credentials.mdp
        )

        if not utilisateur_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou mot de passe incorrect",
            )

        user_service = UserService()
        utilisateur = user_service.user_dao.trouver_par_id(utilisateur_id)

        if not utilisateur:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé",
            )

        token_data = sign_jwt(id_utilisateur=utilisateur.id_utilisateur)

        return LoginResponse(
            access_token=token_data["access_token"],
            utilisateur=UtilisateurResponse(
                id_utilisateur=utilisateur.id_utilisateur,
                email=utilisateur.email,
                pseudo=utilisateur.pseudo,
                nom=utilisateur.nom,
                prenom=utilisateur.prenom,
            ),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'authentification : {e}",
        ) from e


@router.post(
    "/signup",
    response_model=LoginResponse,
    summary="Inscription utilisateur",
    description="Crée un nouveau compte utilisateur et retourne un token JWT",
)
async def signup(user_data: SignupRequest):
    user_service = UserService()

    try:
        utilisateur = user_service.creer_utilisateur(
            email=user_data.email,
            pseudo=user_data.pseudo,
            mdp=user_data.mdp,
            nom=user_data.nom,
            prenom=user_data.prenom,
        )

        if not utilisateur:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Impossible de créer l'utilisateur (email ou pseudo déjà utilisé)",
            )

        token_data = sign_jwt(id_utilisateur=utilisateur.id_utilisateur)

        return LoginResponse(
            access_token=token_data["access_token"],
            utilisateur=UtilisateurResponse(
                id_utilisateur=utilisateur.id_utilisateur,
                email=utilisateur.email,
                pseudo=utilisateur.pseudo,
                nom=utilisateur.nom,
                prenom=utilisateur.prenom,
            ),
        )

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve),
        ) from ve
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du compte : {e}",
        ) from e


@router.get(
    "/me",
    response_model=UtilisateurResponse,
    summary="Informations utilisateur connecté",
    description="Récupère les informations de l'utilisateur authentifié",
    dependencies=[Depends(JWTBearer())],
)
async def get_current_user(token: str = Depends(JWTBearer())):
    try:
        utilisateur_data = get_utilisateur_from_token(token)

        if not utilisateur_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé",
            )

        return utilisateur_data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des informations : {e}",
        ) from e


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Déconnexion utilisateur",
    description="Déconnecte l'utilisateur (côté client)",
    dependencies=[Depends(JWTBearer())],
)
async def logout():
    return MessageResponse(
        message="Déconnexion réussie. Supprimez le token côté client."
    )
