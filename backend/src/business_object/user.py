from datetime import datetime
from typing import Optional
import re


class User:
    """
    Classe représentant un utilisateur

    Attributs
    ----------
    id_utilisateur : int
        identifiant de l'utilisateur.
    email : str
        email de l'utilisateur.
    pseudo : str
        pseudo de l'utilisateur.
    mdp_hash : str
        Le hash du mot de passe de l'utilisateur.
    nom : str
        Le nom de l'utilisateur.
    prenom : str
        Le Prénom de l'utilisateur.
    date_creation : datetime
        La date de création de l'utilisateur.
    date_derniere_connexion : datetime
        La date de la dernière connexion de l'utilisateur.
    """

    def __init__(
        self,
        id_utilisateur: int,
        email: str,
        pseudo: str,
        mdp_hash: str,
        nom: str,
        prenom: str,
        date_creation: Optional[datetime] = None,
        date_derniere_connexion: Optional[datetime] = None,
    ):
        self.id_utilisateur = id_utilisateur
        self.email = email
        self.pseudo = pseudo
        self.mdp_hash = mdp_hash
        self.nom = nom
        self.prenom = prenom
        self.date_creation = date_creation or datetime.now()
        self.date_derniere_connexion = date_derniere_connexion

    def valider_email(self) -> bool:
        """Valide le format de l'email"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, self.email) is not None

