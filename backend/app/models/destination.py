from __future__ import annotations

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Destination(Base):
    __tablename__ = "destinations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128), index=True)
    city: Mapped[str] = mapped_column(String(64), default="")
    category: Mapped[str] = mapped_column(String(32), index=True)
    district: Mapped[str] = mapped_column(String(64), default="")
    address: Mapped[str] = mapped_column(String(256), default="")
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    heat: Mapped[float | None] = mapped_column(Float, nullable=True)
    heat_metric: Mapped[str] = mapped_column(String(64), default="")
    tags: Mapped[str] = mapped_column(String(512), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    image_url: Mapped[str] = mapped_column(String(256), default="")
    image_source_name: Mapped[str] = mapped_column(String(128), default="")
    image_source_url: Mapped[str] = mapped_column(String(256), default="")
    source_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source_url: Mapped[str | None] = mapped_column(String(256), nullable=True)
    fetched_date: Mapped[str | None] = mapped_column(String(32), nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    rating_source_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    rating_source_url: Mapped[str | None] = mapped_column(String(256), nullable=True)
    heat_source_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    heat_source_url: Mapped[str | None] = mapped_column(String(256), nullable=True)


class Scene(Base):
    __tablename__ = "scenes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    label: Mapped[str] = mapped_column(String(128), default="")
    city: Mapped[str] = mapped_column(String(64), default="")
    supports_routing: Mapped[bool] = mapped_column(Boolean, default=True)

    nodes: Mapped[list[SceneNode]] = relationship(back_populates="scene")
    buildings: Mapped[list[Building]] = relationship(back_populates="scene")
    facilities: Mapped[list[Facility]] = relationship(back_populates="scene")
    edges: Mapped[list[Edge]] = relationship(back_populates="scene")


class SceneNode(Base):
    __tablename__ = "scene_nodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    scene_id: Mapped[int] = mapped_column(Integer, ForeignKey("scenes.id"))
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    scene: Mapped[Scene] = relationship(back_populates="nodes")


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    scene_id: Mapped[int] = mapped_column(Integer, ForeignKey("scenes.id"))
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    building_type: Mapped[str] = mapped_column(String(64))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    scene: Mapped[Scene] = relationship(back_populates="buildings")


class Facility(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    scene_id: Mapped[int] = mapped_column(Integer, ForeignKey("scenes.id"))
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    facility_type: Mapped[str] = mapped_column(String(64), index=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    scene: Mapped[Scene] = relationship(back_populates="facilities")


class Edge(Base):
    __tablename__ = "edges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    scene_id: Mapped[int] = mapped_column(Integer, ForeignKey("scenes.id"))
    source_code: Mapped[str] = mapped_column(String(64), index=True)
    target_code: Mapped[str] = mapped_column(String(64), index=True)
    distance: Mapped[float] = mapped_column(Float)
    congestion: Mapped[float] = mapped_column(Float, default=1.0)
    walk_speed: Mapped[float] = mapped_column(Float, default=1.1)
    bike_speed: Mapped[float] = mapped_column(Float, default=3.5)
    shuttle_speed: Mapped[float] = mapped_column(Float, default=4.8)
    allowed_modes: Mapped[str] = mapped_column(String(128), default="walk")

    scene: Mapped[Scene] = relationship(back_populates="edges")
