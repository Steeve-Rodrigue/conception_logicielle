"""Script de réinitialisation de la base de données."""

import sys
from pathlib import Path

from dotenv import load_dotenv
from src.utils.singleton import Singleton
from src.dao.db_connection import DBConnection

src_path = Path(__file__).resolve().parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


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
            base_path = Path(__file__).resolve().parent.parent
            init_db_path = base_path.parent / "data" / "init_db.sql"
            pop_db_path = base_path.parent / "data" / "pop_db.sql"

            if not init_db_path.exists():
                raise FileNotFoundError(f"Fichier non trouvé: {init_db_path}")
            if not pop_db_path.exists():
                raise FileNotFoundError(f"Fichier non trouvé: {pop_db_path}")

            print(f"📁 Lecture de {init_db_path}")
            with open(init_db_path, encoding="utf-8") as f:
                init_sql = f.read()

            print(f"📁 Lecture de {pop_db_path}")
            with open(pop_db_path, encoding="utf-8") as f:
                pop_sql = f.read()

            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    init_queries = [q.strip() for q in init_sql.split(";") if q.strip()]
                    pop_queries = [q.strip() for q in pop_sql.split(";") if q.strip()]

                    print(
                        f"🔧 Exécution de {len(init_queries)} requêtes d'initialisation..."
                    )
                    for i, query in enumerate(init_queries, 1):
                        try:
                            cursor.execute(query)
                            print(f"   ✓ Requête {i}/{len(init_queries)} exécutée")
                        except Exception as e:
                            print(f"   ✗ Erreur requête {i}: {e}")
                            raise

                    print(
                        f"📊 Exécution de {len(pop_queries)} requêtes de population..."
                    )
                    for i, query in enumerate(pop_queries, 1):
                        try:
                            cursor.execute(query)
                            print(f"   ✓ Requête {i}/{len(pop_queries)} exécutée")
                        except Exception as e:
                            print(f"   ✗ Erreur requête {i}: {e}")
                            raise

                connection.commit()

            print("=" * 70)
            print("✅ RÉINITIALISATION TERMINÉE AVEC SUCCÈS")
            print("=" * 70)
            return True

        except FileNotFoundError as e:
            print(f"❌ ERREUR - Fichier manquant: {e}")
            raise
        except Exception as e:
            print(f"❌ ERREUR - Base de données: {e}")
            raise


if __name__ == "__main__":
    try:
        ResetDatabase().lancer()
    except Exception:
        sys.exit(1)
