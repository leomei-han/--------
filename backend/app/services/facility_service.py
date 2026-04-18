from __future__ import annotations

from app.repositories.data_loader import DatasetRepository
from app.services.routing_service import RoutePlanningService


class NearbyFacilityService:
    def __init__(self, repository: DatasetRepository) -> None:
        self.repository = repository
        self.route_service = RoutePlanningService(repository)

    def nearby(self, scene_name: str, origin_code: str, category: str | None = None, radius: float = 1200.0) -> list[dict]:
        facilities = [item for item in self.repository.facilities() if item["scene_name"] == scene_name]
        if category:
            facilities = [item for item in facilities if item["facility_type"] == category]

        ranked = []
        for facility in facilities:
            route = self.route_service.plan_single(scene_name, origin_code, facility["code"], "distance", "walk")
            if route["path_codes"] and route["total_distance_m"] <= radius:
                ranked.append({**facility, "graph_distance": route["total_distance_m"]})
        ranked.sort(key=lambda item: item["graph_distance"])
        return ranked
