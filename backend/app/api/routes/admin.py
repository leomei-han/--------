from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()


@router.get("/status")
def import_status() -> dict:
    settings = get_settings()
    return {
        "dataset_dir": str(settings.dataset_dir),
        "files": [item.name for item in settings.dataset_dir.glob("*.json")],
    }
