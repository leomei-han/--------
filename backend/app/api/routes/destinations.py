from fastapi import APIRouter, Depends

from app.repositories.data_loader import DatasetRepository, get_repository
from app.schemas.destination import DestinationSearchResponse, RecommendationRequest, SearchRequest
from app.services.recommendation_service import RecommendationService
from app.services.search_service import SearchService

router = APIRouter()


@router.get("")
def list_destinations(repository: DatasetRepository = Depends(get_repository)) -> list[dict]:
    return repository.destinations()


@router.get("/featured")
def featured_destinations(repository: DatasetRepository = Depends(get_repository), top_k: int | None = None) -> list[dict]:
    return RecommendationService(repository).featured_destinations(top_k)


@router.post("/recommend")
def recommend(payload: RecommendationRequest, repository: DatasetRepository = Depends(get_repository)) -> list[dict]:
    service = RecommendationService(repository)
    return service.recommend_destinations(payload.top_k, payload.category, payload.interest_tags)


@router.post("/search", response_model=DestinationSearchResponse)
def search(payload: SearchRequest, repository: DatasetRepository = Depends(get_repository)) -> DestinationSearchResponse:
    service = SearchService(repository)
    exact = service.exact_search(payload.query)
    fuzzy = service.fuzzy_search(payload.query, payload.keywords, payload.category)
    featured = [
        item
        for item in RecommendationService(repository).featured_destinations(None)
        if payload.query.lower() in item["name"].lower()
    ]
    return DestinationSearchResponse(exact=exact, fuzzy=fuzzy, featured=featured)
