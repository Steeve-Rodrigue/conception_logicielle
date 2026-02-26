"""
Middleware d'authentification JWT pour FastAPI.
Ce fichier contient la classe pour protéger les routes :
- JWTBearer : Pour les routes nécessitant une connexion
"""
import logging

from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.auth.auth_handler import decode_jwt
from src.exceptions import (
    TokenManquantException,
    TokenSchemeInvalideException,
    TokenInvalideException,
)

logger = logging.getLogger(__name__)


class JWTBearer(HTTPBearer):
    """
    Protège les routes : vérifie que l'utilisateur a un token JWT valide.
    """

    def __init__(self, auto_error: bool = True):
        """Initialise le vérificateur de token."""
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        """
        Vérifie le token JWT dans l'en-tête Authorization.

        Returns
        -------
        str
            Le token validé

        Raises
        ------
        TokenSchemeInvalideException
            Si le schéma n'est pas Bearer
        TokenInvalideException
            Si le token est invalide ou expiré
        TokenManquantException
            Si le token est absent
        """
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise TokenSchemeInvalideException()
            if not self.verify_jwt(credentials.credentials):
                raise TokenInvalideException()
            return credentials.credentials

        raise TokenManquantException()

    def verify_jwt(self, jwtoken: str) -> bool:
        """
        Vérifie si un token JWT est valide.

        Parameters
        ----------
        jwtoken : str
            Le token à vérifier

        Returns
        -------
        bool
            True si valide, False sinon
        """
        try:
            payload = decode_jwt(jwtoken)
            return payload is not None
        except Exception as e:
            logger.error("Erreur vérification token : %s", e)
            return False
