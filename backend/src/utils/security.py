"""
Module de gestion de la sécurité.
Hachage bcrypt et validation des mots de passe.
"""

import re
import secrets
import string
import bcrypt


def hash_password(plain_password: str) -> str:
    """Hache un mot de passe avec bcrypt."""
    
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie qu'un mot de passe correspond à son hash."""
    
    try:
          return bcrypt.checkpw(
              plain_password.encode('utf-8'),
              hashed_password.encode('utf-8')
          )
    except (ValueError, AttributeError):
        return False
        


def generate_random_password(length: int = 12) -> str:
    """Génère un mot de passe aléatoire sécurisé."""
    
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def validate_password_strength(user_password: str) -> tuple[bool, str]:
    """Valide la force d'un mot de passe."""
    
  if len(user_password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"
  
  if not re.search(r"[A-Z]", user_password):
        return False, "Le mot de passe doit contenir au moins une majuscule"
    
  if not re.search(r"[a-z]", user_password):
        return False, "Le mot de passe doit contenir au moins une minuscule"
    
  if not re.search(r"\d", user_password):
        return False, "Le mot de passe doit contenir au moins un chiffre"
    
  if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", user_password):
        return False, "Le mot de passe doit contenir au moins un caractère spécial"
  
  return True, "Mot de passe valide"
