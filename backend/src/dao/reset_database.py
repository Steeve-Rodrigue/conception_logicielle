"""Script de réinitialisation de la base de données."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
from pathlib import Path
from utils.singleton import Singleton
from dao.db_connection import DBConnection

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)


class ResetDatabase(metaclass=Singleton):
    """Réinitialise la base de données."""
    
    def lancer(self):
        """Exécute les scripts SQL d'initialisation et de population."""
        print("=" * 70)
        print("RÉINITIALISATION DE LA BASE DE DONNÉES")
        print("=" * 70)
        
        try:
            init_db_path = "data/init_db.sql"
            pop_db_path = "data/pop_db.sql"
            
            if not os.path.exists(init_db_path):
                raise FileNotFoundError(f"Fichier non trouvé: {init_db_path}")
            if not os.path.exists(pop_db_path):
                raise FileNotFoundError(f"Fichier non trouvé: {pop_db_path}")
            
            with open(init_db_path, encoding="utf-8") as f:
                init_sql = f.read()
            with open(pop_db_path, encoding="utf-8") as f:
                pop_sql = f.read()
            
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    init_queries = [q.strip() for q in init_sql.split(';') if q.strip()]
                    pop_queries = [q.strip() for q in pop_sql.split(';') if q.strip()]
                    
                    print(f"Exécution de {len(init_queries)} requêtes d'initialisation...")
                    for query in init_queries:
                        cursor.execute(query)
                    
                    print(f"Exécution de {len(pop_queries)} requêtes de population...")
                    for query in pop_queries:
                        cursor.execute(query)
                
                connection.commit()
            
            print("=" * 70)
            print("✅ RÉINITIALISATION TERMINÉE")
            print("=" * 70)
            return True
            
        except Exception as e:
            print(f"❌ ERREUR: {e}")
            raise


if __name__ == "__main__":
    ResetDatabase().lancer()
