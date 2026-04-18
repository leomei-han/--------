from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Destination(Base):
    __tablename__ = "destinations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128), index=True)
    category: Mapped[str] = mapped_column(String(32), index=True)
    district: Mapped[str] = mapped_column(String(64), default="")
    address: Mapped[str] = mapped_column(String(256), default="")
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    heat: Mapped[float | None] = mapped_column(Float, nullable=True)
    tags: Mapped[str] = mapped_column(String(256), default="")
    description: Mapped[str] = mapped_column(Text, default="")

    scenes: Mapped[list["Scene"]] = relationship(back_populates="destination")


class Scene(Base):
    __tablename__ = "scenes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    destination_id: Mapped[int] = mapped_column(ForeignKey("destinations.id"))
    name: Mapped[str] = mapped_column(String(128))
    scene_type: Mapped[str] = mapped_column(String(32))

    destination: Mapped["Destination"] = relationship(back_populates="scenes")
    buildings: Mapped[list["Building"]] = relationship(back_populates="scene")
    facilities: Mapped[list["Facility"]] = relationship(back_populates="scene")
    roads: Mapped[list["Road"]] = relationship(back_populates="scene")
    edges: Mapped[list["Edge"]] = relationship(back_populates="scene")


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    scene_id: Mapped[int] = mapped_column(ForeignKey("scenes.id"))
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    building_type: Mapped[str] = mapped_column(String(64))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    scene: Mapped["Scene"] = relationship(back_populates="buildings")


class Facility(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    scene_id: Mapped[int] = mapped_column(ForeignKey("scenes.id"))
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128))
    facility_type: Mapped[str] = mapped_column(String(64), index=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    scene: Mapped["Scene"] = relationship(back_populates="facilities")


class Road(Base):
    __tablename__ = "roads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    scene_id: Mapped[int] = mapped_column(ForeignKey("scenes.id"))
    road_type: Mapped[str] = mapped_column(String(64))
    transport_modes: Mapped[str] = mapped_column(String(128), default="walk")

    scene: Mapped["Scene"] = relationship(back_populates="roads")


class Edge(Base):
    __tablename__ = "edges"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    scene_id: Mapped[int] = mapped_column(ForeignKey("scenes.id"))
    source_code: Mapped[str] = mapped_column(String(64), index=True)
    target_code: Mapped[str] = mapped_column(String(64), index=True)
    distance: Mapped[float] = mapped_column(Float)
    congestion: Mapped[float] = mapped_column(Float, default=1.0)
    walk_speed: Mapped[float] = mapped_column(Float, default=1.1)
    bike_speed: Mapped[float] = mapped_column(Float, default=3.5)
    shuttle_speed: Mapped[float] = mapped_column(Float, default=4.8)
    allowed_modes: Mapped[str] = mapped_column(String(128), default="walk")

    scene: Mapped["Scene"] = relationship(back_populates="edges")


class FoodPOI(Base):
    __tablename__ = "food_pois"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    destination_id: Mapped[int] = mapped_column(ForeignKey("destinations.id"))
    name: Mapped[str] = mapped_column(String(128), index=True)
    cuisine: Mapped[str] = mapped_column(String(64), index=True)
    venue_name: Mapped[str] = mapped_column(String(128), default="")
    distance_hint: Mapped[float] = mapped_column(Float, default=0.0)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    heat: Mapped[float | None] = mapped_column(Float, nullable=True)
