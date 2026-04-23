from __future__ import annotations

import json
from collections import defaultdict

from sqlalchemy import delete, select
from sqlalchemy.orm import sessionmaker

from app.models import (
    Building,
    Destination,
    Diary,
    DiaryRating,
    Edge,
    Facility,
    Food,
    IndoorBuilding,
    IndoorEdge,
    IndoorNode,
    Scene,
    SceneNode,
    Session as UserSession,
    User,
    UserFavoriteDestination,
    UserFavoriteRoute,
)


def _csv_to_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [item for item in value.split(",") if item]


def _json_text_to_list(value: str | None) -> list:
    if not value:
        return []
    try:
        loaded = json.loads(value)
        if isinstance(loaded, list):
            return loaded
    except json.JSONDecodeError:
        pass
    return []


def _list_to_json_text(value: list | tuple | None) -> str:
    return json.dumps(list(value or []), ensure_ascii=False)


class PostgresRepository:
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    def _destination_to_dict(self, item: Destination) -> dict:
        return {
            "source_id": item.source_id,
            "name": item.name,
            "city": item.city,
            "category": item.category,
            "district": item.district,
            "address": item.address,
            "latitude": item.latitude,
            "longitude": item.longitude,
            "rating": item.rating,
            "heat": item.heat,
            "heat_metric": item.heat_metric,
            "tags": _csv_to_list(item.tags),
            "description": item.description,
            "image_url": item.image_url,
            "image_source_name": item.image_source_name,
            "image_source_url": item.image_source_url,
            "source_name": item.source_name,
            "source_url": item.source_url,
            "fetched_date": item.fetched_date,
            "rating_source_name": item.rating_source_name,
            "rating_source_url": item.rating_source_url,
            "heat_source_name": item.heat_source_name,
            "heat_source_url": item.heat_source_url,
        }

    def destinations(self) -> list[dict]:
        with self._session_factory() as db:
            items = db.scalars(select(Destination).order_by(Destination.id)).all()
            return [self._destination_to_dict(item) for item in items]

    def featured_destinations(self) -> list[dict]:
        with self._session_factory() as db:
            items = db.scalars(
                select(Destination).where(Destination.is_featured.is_(True)).order_by(Destination.id)
            ).all()
            return [self._destination_to_dict(item) for item in items]

    def scenes(self) -> list[dict]:
        with self._session_factory() as db:
            scenes = db.scalars(select(Scene).order_by(Scene.id)).all()
            nodes = db.scalars(select(SceneNode).order_by(SceneNode.id)).all()

            scene_nodes: dict[int, list[dict]] = defaultdict(list)
            for node in nodes:
                scene_nodes[node.scene_id].append(
                    {
                        "code": node.code,
                        "name": node.name,
                        "latitude": node.latitude,
                        "longitude": node.longitude,
                    }
                )

            return [
                {
                    "name": scene.name,
                    "label": scene.label,
                    "city": scene.city,
                    "supports_routing": scene.supports_routing,
                    "nodes": scene_nodes.get(scene.id, []),
                }
                for scene in scenes
            ]

    def buildings(self) -> list[dict]:
        with self._session_factory() as db:
            scenes = {item.id: item.name for item in db.scalars(select(Scene)).all()}
            items = db.scalars(select(Building).order_by(Building.id)).all()
            return [
                {
                    "code": item.code,
                    "name": item.name,
                    "latitude": item.latitude,
                    "longitude": item.longitude,
                    "scene_name": scenes.get(item.scene_id, ""),
                    "building_type": item.building_type,
                }
                for item in items
            ]

    def facilities(self) -> list[dict]:
        with self._session_factory() as db:
            scenes = {item.id: item.name for item in db.scalars(select(Scene)).all()}
            items = db.scalars(select(Facility).order_by(Facility.id)).all()
            return [
                {
                    "scene_name": scenes.get(item.scene_id, ""),
                    "code": item.code,
                    "name": item.name,
                    "facility_type": item.facility_type,
                    "latitude": item.latitude,
                    "longitude": item.longitude,
                }
                for item in items
            ]

    def edges(self) -> list[dict]:
        with self._session_factory() as db:
            scenes = {item.id: item.name for item in db.scalars(select(Scene)).all()}
            items = db.scalars(select(Edge).order_by(Edge.id)).all()
            return [
                {
                    "scene_name": scenes.get(item.scene_id, ""),
                    "source_code": item.source_code,
                    "target_code": item.target_code,
                    "distance": item.distance,
                    "congestion": item.congestion,
                    "walk_speed": item.walk_speed,
                    "bike_speed": item.bike_speed,
                    "shuttle_speed": item.shuttle_speed,
                    "allowed_modes": _csv_to_list(item.allowed_modes) or ["walk"],
                }
                for item in items
            ]

    def indoors(self) -> list[dict]:
        with self._session_factory() as db:
            buildings = db.scalars(select(IndoorBuilding).order_by(IndoorBuilding.id)).all()
            nodes = db.scalars(select(IndoorNode).order_by(IndoorNode.id)).all()
            edges = db.scalars(select(IndoorEdge).order_by(IndoorEdge.id)).all()

            nodes_by_building: dict[int, list[dict]] = defaultdict(list)
            for node in nodes:
                nodes_by_building[node.building_id].append(
                    {
                        "code": node.code,
                        "name": node.name,
                        "floor": node.floor,
                        "node_type": node.node_type,
                    }
                )

            edges_by_building: dict[int, list[dict]] = defaultdict(list)
            for edge in edges:
                edges_by_building[edge.building_id].append(
                    {
                        "source": edge.source_code,
                        "target": edge.target_code,
                        "distance": edge.distance,
                        "kind": edge.kind,
                        "wait_seconds": edge.wait_seconds,
                        "bidirectional": edge.bidirectional,
                    }
                )

            return [
                {
                    "building_code": item.building_code,
                    "building_name": item.building_name,
                    "scene_name": item.scene_name,
                    "nodes": nodes_by_building.get(item.id, []),
                    "edges": edges_by_building.get(item.id, []),
                }
                for item in buildings
            ]

    def foods(self) -> list[dict]:
        with self._session_factory() as db:
            items = db.scalars(select(Food).order_by(Food.id)).all()
            return [
                {
                    "source_id": item.source_id,
                    "name": item.name,
                    "city": item.city,
                    "destination_name": item.destination_name,
                    "cuisine": item.cuisine,
                    "venue_name": item.venue_name,
                    "latitude": item.latitude,
                    "longitude": item.longitude,
                    "rating": item.rating,
                    "heat": item.heat,
                    "heat_metric": item.heat_metric,
                    "source_name": item.source_name,
                    "source_url": item.source_url,
                    "description": item.description,
                    "image_url": item.image_url,
                    "image_source_name": item.image_source_name,
                    "image_source_url": item.image_source_url,
                    "fetched_date": item.fetched_date,
                }
                for item in items
            ]

    def diaries(self) -> list[dict]:
        with self._session_factory() as db:
            items = db.scalars(select(Diary).order_by(Diary.id)).all()
            return [
                {
                    "id": item.id,
                    "title": item.title,
                    "destination_name": item.destination_name,
                    "content": item.content,
                    "views": item.views,
                    "rating": item.rating,
                    "media_urls": _json_text_to_list(item.media_urls),
                    "author_id": item.author_id,
                    "author_name": item.author_name,
                    "created_at": item.created_at,
                }
                for item in items
            ]

    def diary_ratings(self) -> list[dict]:
        with self._session_factory() as db:
            items = db.scalars(select(DiaryRating).order_by(DiaryRating.id)).all()
            return [
                {
                    "id": item.id,
                    "diary_id": item.diary_id,
                    "user_id": item.user_id,
                    "score": item.score,
                    "updated_at": item.updated_at,
                }
                for item in items
            ]

    def users(self) -> list[dict]:
        with self._session_factory() as db:
            users = db.scalars(select(User).order_by(User.id)).all()
            favorite_destinations = db.scalars(
                select(UserFavoriteDestination).order_by(UserFavoriteDestination.id)
            ).all()
            favorite_routes = db.scalars(select(UserFavoriteRoute).order_by(UserFavoriteRoute.id)).all()

            favorite_destinations_by_user: dict[int, list[str]] = defaultdict(list)
            for item in favorite_destinations:
                favorite_destinations_by_user[item.user_id].append(item.destination_source_id)

            favorite_routes_by_user: dict[int, list[dict]] = defaultdict(list)
            for item in favorite_routes:
                favorite_routes_by_user[item.user_id].append(
                    {
                        "scene_name": item.scene_name,
                        "strategy": item.strategy,
                        "transport_mode": item.transport_mode,
                        "path_codes": _json_text_to_list(item.path_codes),
                        "path_names": _json_text_to_list(item.path_names),
                        "total_distance_m": item.total_distance_m,
                        "estimated_minutes": item.estimated_minutes,
                        "explanation": item.explanation,
                        "saved_at": item.saved_at,
                    }
                )

            return [
                {
                    "id": item.id,
                    "username": item.username,
                    "display_name": item.display_name,
                    "interests": item.interests,
                    "password_hash": item.password_hash,
                    "created_at": item.created_at,
                    "last_login_at": item.last_login_at,
                    "favorite_destination_ids": favorite_destinations_by_user.get(item.id, []),
                    "favorite_route_snapshots": favorite_routes_by_user.get(item.id, []),
                }
                for item in users
            ]

    def sessions(self) -> list[dict]:
        with self._session_factory() as db:
            items = db.scalars(select(UserSession).order_by(UserSession.id)).all()
            return [
                {
                    "token": item.token,
                    "user_id": item.user_id,
                    "created_at": item.created_at,
                }
                for item in items
            ]

    def save_users(self, payload: list[dict]) -> None:
        with self._session_factory() as db:
            with db.begin():
                existing_users = {item.id: item for item in db.scalars(select(User)).all()}

                for item in payload:
                    user_id = int(item["id"])
                    user = existing_users.get(user_id)
                    if user is None:
                        user = User(id=user_id, username=str(item["username"]))
                        db.add(user)

                    user.username = str(item["username"])
                    user.display_name = str(item.get("display_name") or item["username"])
                    user.interests = str(item.get("interests") or "")
                    user.password_hash = str(item.get("password_hash") or "")
                    user.created_at = str(item.get("created_at") or "")
                    user.last_login_at = str(item.get("last_login_at") or "")

                db.flush()

                for item in payload:
                    user_id = int(item["id"])
                    db.execute(delete(UserFavoriteDestination).where(UserFavoriteDestination.user_id == user_id))
                    db.execute(delete(UserFavoriteRoute).where(UserFavoriteRoute.user_id == user_id))

                    for source_id in item.get("favorite_destination_ids", []):
                        db.add(
                            UserFavoriteDestination(
                                user_id=user_id,
                                destination_source_id=str(source_id),
                            )
                        )

                    for snapshot in item.get("favorite_route_snapshots", []):
                        db.add(
                            UserFavoriteRoute(
                                user_id=user_id,
                                scene_name=str(snapshot.get("scene_name") or ""),
                                strategy=str(snapshot.get("strategy") or ""),
                                transport_mode=str(snapshot.get("transport_mode") or ""),
                                path_codes=_list_to_json_text(snapshot.get("path_codes")),
                                path_names=_list_to_json_text(snapshot.get("path_names")),
                                total_distance_m=float(snapshot.get("total_distance_m") or 0.0),
                                estimated_minutes=float(snapshot.get("estimated_minutes") or 0.0),
                                explanation=str(snapshot.get("explanation") or ""),
                                saved_at=str(snapshot.get("saved_at") or ""),
                            )
                        )

    def save_sessions(self, payload: list[dict]) -> None:
        with self._session_factory() as db:
            with db.begin():
                db.execute(delete(UserSession))
                for item in payload:
                    db.add(
                        UserSession(
                            token=str(item["token"]),
                            user_id=int(item["user_id"]),
                            created_at=str(item.get("created_at") or ""),
                        )
                    )

    def save_diaries(self, payload: list[dict]) -> None:
        with self._session_factory() as db:
            with db.begin():
                existing_diaries = {item.id: item for item in db.scalars(select(Diary)).all()}
                payload_ids = {int(item["id"]) for item in payload}

                if payload_ids:
                    removed_ids = set(existing_diaries.keys()) - payload_ids
                    if removed_ids:
                        db.execute(delete(DiaryRating).where(DiaryRating.diary_id.in_(removed_ids)))
                        db.execute(delete(Diary).where(Diary.id.in_(removed_ids)))
                else:
                    db.execute(delete(DiaryRating))
                    db.execute(delete(Diary))

                for item in payload:
                    diary_id = int(item["id"])
                    diary = existing_diaries.get(diary_id)
                    if diary is None:
                        diary = Diary(id=diary_id, title=str(item.get("title") or ""), content="")
                        db.add(diary)

                    diary.title = str(item.get("title") or "")
                    diary.destination_name = str(item.get("destination_name") or "")
                    diary.content = str(item.get("content") or "")
                    diary.views = int(item.get("views") or 0)
                    diary.rating = float(item.get("rating") or 0.0)
                    diary.media_urls = _list_to_json_text(item.get("media_urls"))
                    diary.author_id = int(item.get("author_id") or 0)
                    diary.author_name = str(item.get("author_name") or "")
                    diary.created_at = str(item.get("created_at") or "")

    def save_diary_ratings(self, payload: list[dict]) -> None:
        with self._session_factory() as db:
            with db.begin():
                existing_items = {item.id: item for item in db.scalars(select(DiaryRating)).all()}
                payload_ids = {int(item["id"]) for item in payload}

                if payload_ids:
                    removed_ids = set(existing_items.keys()) - payload_ids
                    if removed_ids:
                        db.execute(delete(DiaryRating).where(DiaryRating.id.in_(removed_ids)))
                else:
                    db.execute(delete(DiaryRating))

                for item in payload:
                    rating_id = int(item["id"])
                    rating = existing_items.get(rating_id)
                    if rating is None:
                        rating = DiaryRating(id=rating_id, diary_id=int(item["diary_id"]), user_id=int(item["user_id"]))
                        db.add(rating)

                    rating.diary_id = int(item["diary_id"])
                    rating.user_id = int(item["user_id"])
                    rating.score = float(item.get("score") or 0.0)
                    rating.updated_at = str(item.get("updated_at") or "")
