"""Script de réinitialisation de la base de données et import France Travail."""

import sys
from pathlib import Path
from dotenv import load_dotenv
from src.utils.singleton import Singleton
from src.dao.db_connection import DBConnection
from src.services.france_travail_service import FranceTravailService
from src.dao.job_offer_dao import JobOfferDao
from src.utils.search_terms import TERMES_IA_ML
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

src_path = Path(__file__).resolve().parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)


class ResetDatabase(metaclass=Singleton):
    """Réinitialise la base et importe les offres France Travail."""

    def lancer(self, limit_par_motcle=1000):
        """Exécute les scripts SQL d'initialisation et de population."""
        logger.info("=" * 70)
        logger.info("RÉINITIALISATION DE LA BASE DE DONNÉES")
        logger.info("=" * 70)

        try:
            base_path = Path(__file__).resolve().parent.parent
            init_db_path = base_path.parent / "data" / "init_db.sql"

            if not init_db_path.exists():
                raise FileNotFoundError(f"Fichier non trouvé: {init_db_path}")

            logger.info(f"Lecture de {init_db_path}")
            with open(init_db_path, encoding="utf-8") as f:
                init_sql = f.read()

            # Exécution des requêtes init
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    init_queries = [q.strip() for q in init_sql.split(";") if q.strip()]
                    logger.info(f"Exécution de {len(init_queries)} requêtes d'initialisation...")
                    for i, query in enumerate(init_queries, 1):
                        cursor.execute(query)
            connection.commit()
            logger.info("Initialisation SQL terminée")

            # Import France Travail
            logger.info("Récupération des offres France Travail...")
            service = FranceTravailService()
            dao = JobOfferDao()

            total_inserted = 0

            for mot in TERMES_IA_ML:
                offres = service.rechercher_offres(
                    mots_cles=mot,
                    departement=None,  
                    limit=limit_par_motcle
                )

                inserted = 0
                for offre in offres:
                    if dao.creer_offre(offre):
                        inserted += 1

                total_inserted += inserted
                logger.info(f" {inserted} offres insérées pour '{mot}'")

            logger.info(f"\n TOTAL OFFRES INSÉRÉES: {total_inserted}")
            logger.info("=" * 70)
            logger.info(" RÉINITIALISATION ET IMPORT TERMINÉS")
            logger.info("=" * 70)

            return True

        except FileNotFoundError as e:
            logger.error(f" Fichier manquant: {e}")
            raise
        except Exception as e:
            logger.error(f" Erreur base de données / import: {e}")
            raise


if __name__ == "__main__":
    try:
        ResetDatabase().lancer()
    except Exception:
        sys.exit(1)
