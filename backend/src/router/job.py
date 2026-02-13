from fastapi import APIRouter, HTTPException, Query, BackgroundTasks, status
from pydantic import BaseModel, Field
from typing import Optional
from src.services.job_aggregation_service import JobAggregationService


# 1. ON DÉFINIT LES MODÈLES D'ABORD (Le "moule" pour les données reçues)
class SyncRequest(BaseModel):
    mots_cles: str = Field("développeur", description="Mots-clés à chercher")
    localisation: Optional[str] = Field(None, description="Code postal ou ville")


# 2. ON INITIALISE LE ROUTER ET LE SERVICE
router = APIRouter(prefix="/jobs", tags=["Offres d'Emploi"])
job_service = JobAggregationService()

# 3. LES POINTS D'ENTRÉE (ENDPOINTS)


@router.get("/", summary="Rechercher des offres")
def get_all_jobs(
    q: Optional[str] = Query(None, description="Recherche par mots-clés"),
    localisation: Optional[str] = Query(None, description="Filtrer par ville"),
    limit: int = Query(20, ge=1, le=100),
):
    """Récupère les offres déjà présentes dans ta base PostgreSQL."""
    offers = job_service.rechercher_offres_locales(
        mots_cles=q, localisation=localisation, limit=limit
    )
    return {"total": len(offers), "results": [o.to_dict() for o in offers]}


@router.post(
    "/sync",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Synchroniser avec France Travail",
)
def sync_jobs(sync_params: SyncRequest, background_tasks: BackgroundTasks):
    """
    Lance la récupération des offres France Travail.
    C'est asynchrone : on répond 'OK' tout de suite, et le travail se fait derrière.
    """
    background_tasks.add_task(
        job_service.synchroniser_offres,
        mots_cles=sync_params.mots_cles,
        localisation=sync_params.localisation,
    )
    return {
        "status": "en cours",
        "message": "La base de données est en train de se remplir.",
    }


@router.get("/{id_offre}", summary="Voir une offre précise")
def get_job_details(id_offre: int):
    offer = job_service.job_offer_dao.trouver_par_id(id_offre)
    if not offer:
        raise HTTPException(status_code=404, detail="Cette offre n'existe pas.")
    return offer.to_dict()
