"""
Routes d'authentification de l'API.

Expose les endpoints pour la connexion, l'inscription,
la déconnexion et la récupération des informations utilisateur.
Utilise JWT pour la gestion des tokens d'authentification.
"""
import logging

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
from src.exceptions import (
    TokenManquantException,
    TokenSchemeInvalideException,
    TokenInvalideException,
    UtilisateurNonTrouveException,
    IdentifiantsInvalidesException,
    UtilisateurDejaExistantException,
)

logger = logging.getLogger(__name__)

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
    """
    Authentifie un utilisateur et génère un token JWT.

    Parameters
    ----------
    credentials : LoginRequest
        Email et mot de passe de l'utilisateur

    Returns
    -------
    LoginResponse
        Token d'accès et informations de l'utilisateur

    Raises
    ------
    HTTPException
        401 si les identifiants sont incorrects
        404 si l'utilisateur n'existe pas
        500 en cas d'erreur interne
    """
    try:
        utilisateur_id = check_utilisateur(
            email=credentials.email, mdp=credentials.mdp
        )

        if not utilisateur_id:
            raise IdentifiantsInvalidesException()

        user_service = UserService()
        utilisateur = user_service.user_dao.trouver_par_id(utilisateur_id)

        if not utilisateur:
            raise UtilisateurNonTrouveException()

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

    except IdentifiantsInvalidesException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
        )
    except UtilisateurNonTrouveException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé",
        )
    except Exception as e:
        logger.error("Erreur lors de l'authentification : %s", e)
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
    """
    Crée un nouveau compte utilisateur.

    Parameters
    ----------
    user_data : SignupRequest
        Informations d'inscription (email, pseudo, mot de passe, confirmation, nom, prénom)

    Returns
    -------
    LoginResponse
        Token d'accès et informations de l'utilisateur

    Raises
    ------
    HTTPException
        400 si l'email ou le pseudo est déjà utilisé
        500 en cas d'erreur interne
    """
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
            raise UtilisateurDejaExistantException()

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

    except UtilisateurDejaExistantException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ou pseudo déjà utilisé",
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve),
        ) from ve
    except Exception as e:
        logger.error("Erreur lors de la création du compte : %s", e)
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
    """
    Récupère les informations de l'utilisateur actuellement connecté.

    Parameters
    ----------
    token : str
        Token JWT de l'utilisateur

    Returns
    -------
    UtilisateurResponse
        Informations de l'utilisateur connecté

    Raises
    ------
    HTTPException
        403 si le token est absent, invalide ou expiré
        404 si l'utilisateur n'existe plus
        500 en cas d'erreur interne
    """
    try:
        utilisateur_data = get_utilisateur_from_token(token)

        if not utilisateur_data:
            raise UtilisateurNonTrouveException()

        return utilisateur_data

    except UtilisateurNonTrouveException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé",
        )
    except TokenSchemeInvalideException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Le schéma doit être 'Bearer <token>'",
        )
    except TokenInvalideException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token invalide ou expiré",
        )
    except TokenManquantException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token manquant",
        )
    except Exception as e:
        logger.error("Erreur récupération utilisateur : %s", e)
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
    """
    Déconnexion de l'utilisateur.

    Note : Avec JWT, la déconnexion est gérée côté client en supprimant le token.

    Returns
    -------
    MessageResponse
        Message de confirmation de déconnexion
    """
    return MessageResponse(
        message="Déconnexion réussie. Supprimez le token côté client."
    )
