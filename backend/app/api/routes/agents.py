from fastapi import APIRouter

from app.services.agent_service import AgentService

router = APIRouter()


@router.get("")
def get_agents() -> dict:
    return AgentService().overview()
