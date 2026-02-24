from fastapi import APIRouter, HTTPException, Query, BackgroundTasks, status
from typing import Optional, List

from src.dao.job_offer_dao import JobOfferDao
from src.dto.job_dto import JobOfferDTO, JobSearchResponse, SyncRequest, SyncResponse
from src.services.job_aggregation_service import JobAggregationService
from src.utils.search_terms import TERMES_IA_ML

router = APIRouter(prefix="/jobs", tags=["Offres d'Emploi"])
job_dao = JobOfferDao()
job_service = JobAggregationService()


@router.get(
    "/",
    response_model=JobSearchResponse,
    summary="Rechercher des offres"
)
def get_all_jobs(
    q: Optional[str] = Query(None, description="Recherche par mots-clés"),
    localisation: Optional[str] = Query(None, description="Filtrer par ville"),
    type_contrat: Optional[str] = Query(None, description="CDI, CDD, Stage..."),
    competence: Optional[str] = Query(None, description="Compétence requise"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Recherche les offres actives avec les filtres disponibles"""
    competences_list = [competence] if competence else None
    offres = job_dao.rechercher_offres(
        mots_cles=q,
        localisation=localisation,
        type_contrat=type_contrat,
        competences=competences_list,
        limit=limit,
        offset=offset,
    )

    return JobSearchResponse(
        total=len(offres),
        results=[JobOfferDTO.model_validate(o) for o in offres]
    )


@router.post(
    "/sync",
    response_model=SyncResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Synchroniser avec France Travail"
)

@router.post("/sync", response_model=SyncResponse, status_code=202)
def sync_jobs(sync_params: SyncRequest, background_tasks: BackgroundTasks):
    termes = [t for t in (sync_params.termes or TERMES_IA_ML) if t and t != "string"]
    departement = sync_params.departement if sync_params.departement and sync_params.departement != "string" else None

    if not termes:
        return SyncResponse(status="erreur", message="Aucun terme de recherche valide fourni")

    background_tasks.add_task(
        job_service.synchroniser_offres,
        termes=termes,
        departement=departement,
    )

    return SyncResponse(
        status="en cours",
        message=f"Synchronisation démarrée pour {len(termes)} termes"
    )


@router.get(
    "/{id_offre}",
    response_model=JobOfferDTO,
    summary="Détails d'une offre"
)
def get_job_details(id_offre: int):
    """Récupère une offre par son ID"""
    offre = job_dao.trouver_par_id(id_offre)
    if not offre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Offre {id_offre} introuvable"
        )
    return JobOfferDTO.model_validate(offre)
