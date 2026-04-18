from fastapi import Depends, Header, HTTPException

from app.repositories.data_loader import DatasetRepository, get_repository
from app.services.auth_service import AuthService


def extract_token(authorization: str | None) -> str | None:
    if not authorization:
        return None
    prefix = "Bearer "
    if authorization.startswith(prefix):
        return authorization[len(prefix) :].strip()
    return authorization.strip() or None


def get_current_user(
    authorization: str | None = Header(default=None),
    repository: DatasetRepository = Depends(get_repository),
) -> dict:
    token = extract_token(authorization)
    user = AuthService(repository).current_user(token)
    if user is None:
        raise HTTPException(status_code=401, detail="请先登录")
    return user
