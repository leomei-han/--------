from __future__ import annotations

from app.algorithms.topk import TopKSelector
from app.repositories.data_loader import DatasetRepository


class RecommendationService:
    def __init__(self, repository: DatasetRepository) -> None:
        self.repository = repository

    @staticmethod
    def _score(item: dict, interest_tags: list[str]) -> float:
        rating = float(item.get("rating") or 0.0)
        heat = float(item.get("heat") or 0.0)
        tags = set(item.get("tags", []))
        interest_bonus = len(tags & set(interest_tags)) * 8
        return rating * 15 + heat * 0.1 + interest_bonus

    def recommend_destinations(self, top_k: int, category: str | None, interest_tags: list[str]) -> list[dict]:
        destinations = self.repository.destinations()
        if category:
            destinations = [item for item in destinations if item["category"] == category]
        selector = TopKSelector(lambda item: self._score(item, interest_tags))
        return selector.select(destinations, top_k)

    def featured_destinations(self, top_k: int | None = None) -> list[dict]:
        featured = self.repository.featured_destinations()
        if top_k is None:
            return featured
        selector = TopKSelector(lambda item: self._score(item, item.get("tags", [])))
        return selector.select(featured, top_k)

    def recommend_foods(self, top_k: int | None, cuisine: str | None = None) -> list[dict]:
        foods = self.repository.foods()
        if cuisine:
            foods = [item for item in foods if item["cuisine"] == cuisine]
        if top_k is None:
            return foods
        selector = TopKSelector(lambda item: float(item.get("rating") or 0.0) * 10 + float(item.get("heat") or 0.0))
        return selector.select(foods, top_k)
