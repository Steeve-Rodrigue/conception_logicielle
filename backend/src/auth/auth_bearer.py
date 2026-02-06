"""
Middleware d'authentification JWT pour FastAPI.

Ce fichier contient 2 classes pour protéger les routes :
- JWTBearer : Pour les routes nécessitant une connexion
- JWTBearerAdmin : Pour les routes réservées aux admins
"""

from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from webservice.auth.auth_handler import decode_jwt, verify_admin


class JWTBearer(HTTPBearer):
    """
    Protège les routes : vérifie que l'utilisateur a un token JWT valide.
    
    Utilisation dans une route :
    @app.get("/ma-route", dependencies=[Depends(JWTBearer())])
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
        HTTPException
            Si le token est absent, invalide ou expiré
        """
        # Récupère les credentials depuis l'en-tête Authorization
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials:
            # Vérifie que c'est bien un token Bearer
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Le schéma doit être 'Bearer <token>'"
                )

            # Vérifie que le token est valide
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Token invalide ou expiré"
                )

            return credentials.credentials

        # Pas de token fourni
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token manquant"
        )

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
            print(f"Erreur vérification token : {e}")
            return False


class JWTBearerAdmin(JWTBearer):
    """
    Protège les routes admin : vérifie le token ET les droits admin.
    
    Utilisation dans une route :
    @app.get("/admin/route", dependencies=[Depends(JWTBearerAdmin())])
    """

    async def __call__(self, request: Request) -> str:
        """
        Vérifie le token JWT ET que l'utilisateur est admin.
        
        Returns
        -------
        str
            Le token validé
            
        Raises
        ------
        HTTPException
            Si le token est invalide OU si l'utilisateur n'est pas admin
        """
        # Vérification standard du token
        token = await super().__call__(request)

        # Vérification des droits admin
        if not verify_admin(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Droits administrateur requis"
            )

        return token
