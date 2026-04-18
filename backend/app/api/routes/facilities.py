from fastapi import APIRouter, Depends, Query

from app.repositories.data_loader import DatasetRepository, get_repository
from app.services.facility_service import NearbyFacilityService

router = APIRouter()


@router.get("/nearby")
def nearby(
    scene_name: str = Query(...),
    origin_code: str = Query(...),
    category: str | None = Query(None),
    radius: float = Query(1200.0),
    repository: DatasetRepository = Depends(get_repository),
) -> list[dict]:
    return NearbyFacilityService(repository).nearby(scene_name, origin_code, category, radius)
