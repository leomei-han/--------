from fastapi import APIRouter, Depends, HTTPException

from app.repositories.data_loader import DatasetRepository, get_repository

router = APIRouter()


@router.get("/scenes")
def scene_list(repository: DatasetRepository = Depends(get_repository)) -> list[dict]:
    return repository.scenes()


@router.get("/scenes/{scene_name}")
def scene_graph(scene_name: str, repository: DatasetRepository = Depends(get_repository)) -> dict:
    scenes = [item for item in repository.scenes() if item["name"] == scene_name]
    if not scenes:
        raise HTTPException(status_code=404, detail="场景不存在")
    buildings = [item for item in repository.buildings() if item["scene_name"] == scene_name]
    facilities = [item for item in repository.facilities() if item["scene_name"] == scene_name]
    edges = [item for item in repository.edges() if item["scene_name"] == scene_name]
    return {"scene": scenes[0], "buildings": buildings, "facilities": facilities, "edges": edges}
