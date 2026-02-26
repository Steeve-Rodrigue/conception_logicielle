"""
Exceptions métier de l'application.
"""


class TokenManquantException(Exception):
    """Levée quand le token JWT est absent."""
    pass


class TokenSchemeInvalideException(Exception):
    """Levée quand le schéma du token n'est pas Bearer."""
    pass


class TokenInvalideException(Exception):
    """Levée quand le token JWT est invalide ou expiré."""
    pass


class UtilisateurNonTrouveException(Exception):
    """Levée quand l'utilisateur n'existe pas."""
    pass


class IdentifiantsInvalidesException(Exception):
    """Levée quand l'email ou le mot de passe est incorrect."""
    pass


class UtilisateurDejaExistantException(Exception):
    """Levée quand l'email ou le pseudo est déjà utilisé."""
    pass
