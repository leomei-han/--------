from fastapi import APIRouter, Depends

from app.repositories.data_loader import DatasetRepository, get_repository
from app.schemas.routing import MultiRouteRequest, SingleRouteRequest
from app.services.routing_service import RoutePlanningService

router = APIRouter()


@router.post("/single")
def single_route(payload: SingleRouteRequest, repository: DatasetRepository = Depends(get_repository)) -> dict:
    service = RoutePlanningService(repository)
    return service.plan_single(payload.scene_name, payload.start_code, payload.end_code, payload.strategy, payload.transport_mode)


@router.post("/multi")
def multi_route(payload: MultiRouteRequest, repository: DatasetRepository = Depends(get_repository)) -> dict:
    service = RoutePlanningService(repository)
    return service.plan_multi(payload.scene_name, payload.start_code, payload.target_codes, payload.strategy, payload.transport_mode)
