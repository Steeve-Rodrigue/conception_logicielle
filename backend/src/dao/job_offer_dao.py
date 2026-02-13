import logging
from typing import Optional, List

from src.business_object.job_offer import JobOffer
from src.dao.db_connection import DBConnection
from src.utils.singleton import Singleton


class JobOfferDao(metaclass=Singleton):
    """DAO pour la gestion des offres d'emploi."""

    def creer_offre(self, offer: JobOffer) -> bool:
        """Crée une offre d'emploi"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO job_offer (
                            external_id, titre, entreprise, description, localisation,
                            type_contrat, salaire, competences_requises, date_publication,
                            url_origine, source, est_active
                        ) VALUES (
                            %(external_id)s, %(titre)s, %(entreprise)s, %(description)s,
                            %(localisation)s, %(type_contrat)s, %(salaire)s,
                            %(competences_requises)s, %(date_publication)s,
                            %(url_origine)s, %(source)s, %(est_active)s
                        )
                        ON CONFLICT (external_id) DO UPDATE SET
                            titre = EXCLUDED.titre,
                            entreprise = EXCLUDED.entreprise,
                            description = EXCLUDED.description,
                            localisation = EXCLUDED.localisation,
                            type_contrat = EXCLUDED.type_contrat,
                            salaire = EXCLUDED.salaire,
                            competences_requises = EXCLUDED.competences_requises,
                            date_publication = EXCLUDED.date_publication,
                            url_origine = EXCLUDED.url_origine,
                            est_active = EXCLUDED.est_active,
                            date_maj = CURRENT_TIMESTAMP
                        RETURNING id_offre;
                        """,
                        {
                            "external_id": offer.external_id,
                            "titre": offer.titre,
                            "entreprise": offer.entreprise,
                            "description": offer.description,
                            "localisation": offer.localisation,
                            "type_contrat": offer.type_contrat,
                            "salaire": offer.salaire,
                            "competences_requises": offer.competences_requises,
                            "date_publication": offer.date_publication,
                            "url_origine": offer.url_origine,
                            "source": offer.source,
                            "est_active": offer.est_active,
                        },
                    )
                    res = cursor.fetchone()
                    if res:
                        offer.id_offre = res["id_offre"]
                        return True
        except Exception as e:
            logging.error(f"Erreur création offre: {e}")
        return False

    def trouver_par_id(self, id_offre: int) -> Optional[JobOffer]:
        """Trouve une offre par son ID"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM job_offer WHERE id_offre = %(id)s;",
                        {"id": id_offre},
                    )
                    res = cursor.fetchone()
                    if res:
                        return self._row_to_offer(res)
        except Exception as e:
            logging.error(f"Erreur recherche offre: {e}")
        return None

    def rechercher_offres(
        self,
        mots_cles: Optional[str] = None,
        localisation: Optional[str] = None,
        type_contrat: Optional[str] = None,
        competences: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[JobOffer]:
        """Recherche des offres avec filtres"""
        try:
            query = "SELECT * FROM job_offer WHERE est_active = TRUE"
            params = {}

            if mots_cles:
                query += " AND (titre ILIKE %(mots_cles)s OR description ILIKE %(mots_cles)s)"
                params["mots_cles"] = f"%{mots_cles}%"

            if localisation:
                query += " AND localisation ILIKE %(localisation)s"
                params["localisation"] = f"%{localisation}%"

            if type_contrat:
                query += " AND type_contrat = %(type_contrat)s"
                params["type_contrat"] = type_contrat

            if competences:
                query += " AND competences_requises && %(competences)s"
                params["competences"] = competences

            query += " ORDER BY date_publication DESC LIMIT %(limit)s OFFSET %(offset)s"
            params["limit"] = limit
            params["offset"] = offset

            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    rows = cursor.fetchall()
                    return [self._row_to_offer(row) for row in rows]
        except Exception as e:
            logging.error(f"Erreur recherche offres: {e}")
        return []

    def desactiver_anciennes_offres(self, jours: int = 30) -> int:
        """Désactive les offres de plus de X jours"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE job_offer
                        SET est_active = FALSE
                        WHERE date_publication < NOW() - INTERVAL '%s days'
                        AND est_active = TRUE;
                        """,
                        (jours,),
                    )
                    return cursor.rowcount
        except Exception as e:
            logging.error(f"Erreur désactivation offres: {e}")
        return 0

    @staticmethod
    def _row_to_offer(row: dict) -> JobOffer:
        """Convertit une ligne SQL en JobOffer"""
        return JobOffer(
            id_offre=row["id_offre"],
            external_id=row["external_id"],
            titre=row["titre"],
            entreprise=row["entreprise"],
            description=row["description"],
            localisation=row["localisation"],
            type_contrat=row["type_contrat"],
            salaire=row.get("salaire"),
            competences_requises=row.get("competences_requises", []),
            date_publication=row["date_publication"],
            url_origine=row.get("url_origine"),
            source=row["source"],
            est_active=row["est_active"],
            date_maj=row["date_maj"],
        )
