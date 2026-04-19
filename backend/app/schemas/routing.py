from pydantic import BaseModel, Field


class RoutePoint(BaseModel):
    code: str


class SingleRouteRequest(BaseModel):
    scene_name: str
    start_code: str
    end_code: str
    strategy: str = "distance"
    transport_mode: str = "walk"
    prefer_nearest_start: bool = False
    start_latitude: float | None = None
    start_longitude: float | None = None


class MultiRouteRequest(BaseModel):
    scene_name: str
    start_code: str
    target_codes: list[str] = Field(default_factory=list)
    strategy: str = "distance"
    transport_mode: str = "walk"
    prefer_nearest_start: bool = False
    start_latitude: float | None = None
    start_longitude: float | None = None


class RouteResponse(BaseModel):
    path: list[str]
    total_distance: float
    total_cost: float
