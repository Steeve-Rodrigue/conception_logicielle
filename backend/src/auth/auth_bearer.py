"""
Middleware d'authentification JWT pour FastAPI.

Ce fichier contient la classe pour protéger les routes :
- JWTBearer : Pour les routes nécessitant une connexion
"""
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.auth.auth_handler import decode_jwt


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
        HTTPException
            Si le token est absent, invalide ou expiré
        """
        
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        
        if credentials:
            
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Le schéma doit être 'Bearer <token>'",
                )
            
            
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Token invalide ou expiré",
                )
            
            return credentials.credentials
        
        
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
