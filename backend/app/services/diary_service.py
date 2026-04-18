from __future__ import annotations

from datetime import datetime

from app.algorithms.compression import HuffmanCodec
from app.algorithms.search import InvertedIndex
from app.algorithms.topk import TopKSelector
from app.repositories.data_loader import DatasetRepository


class DiarySearchService:
    def __init__(self, repository: DatasetRepository) -> None:
        self.repository = repository
        self.inverted = InvertedIndex()
        self._built = False

    def _ensure_index(self) -> None:
        if self._built:
            return
        self.inverted.build(self.repository.diaries(), ["title", "content", "destination_name"], "id")
        self._built = True

    def search(self, query: str) -> list[dict]:
        self._ensure_index()
        ids = self.inverted.search([query])
        items = self.repository.diaries()
        matched = [item for item in items if str(item["id"]) in ids]
        if matched:
            return matched
        normalized = query.strip().lower()
        return [
            item
            for item in items
            if normalized in item["title"].lower()
            or normalized in item["content"].lower()
            or normalized in item["destination_name"].lower()
        ]

    def recommend(self, top_k: int = 10) -> list[dict]:
        selector = TopKSelector(lambda item: item["views"] + item["rating"] * 10)
        return selector.select(self.repository.diaries(), top_k)

    def get_by_id(self, diary_id: int) -> dict | None:
        for item in self.repository.diaries():
            if item["id"] == diary_id:
                return item
        return None

    def create(self, user: dict, payload: dict) -> dict:
        diaries = self.repository.diaries()
        diary = {
            "id": max((item["id"] for item in diaries), default=0) + 1,
            "title": payload["title"],
            "destination_name": payload["destination_name"],
            "content": payload["content"],
            "views": 0,
            "rating": 4.5,
            "media_urls": payload.get("media_urls") or ([payload["cover_image_url"]] if payload.get("cover_image_url") else []),
            "author_id": user["id"],
            "author_name": user["display_name"],
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        diaries.append(diary)
        self.repository.save_diaries(diaries)
        return diary


class CompressionService:
    def __init__(self) -> None:
        self.codec = HuffmanCodec()

    def compress(self, content: str) -> dict:
        encoded, codes = self.codec.encode(content)
        return {"encoded": encoded, "codes": codes}

    def decompress(self, encoded: str, codes: dict[str, str]) -> str:
        return self.codec.decode(encoded, codes)
