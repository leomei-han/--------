from __future__ import annotations

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class IndoorBuilding(Base):
    __tablename__ = "indoor_buildings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    building_code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    building_name: Mapped[str] = mapped_column(String(128), default="")
    scene_name: Mapped[str] = mapped_column(String(128), default="")

    nodes: Mapped[list["IndoorNode"]] = relationship(back_populates="building")
    edges: Mapped[list["IndoorEdge"]] = relationship(back_populates="building")


class IndoorNode(Base):
    __tablename__ = "indoor_nodes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    building_id: Mapped[int] = mapped_column(ForeignKey("indoor_buildings.id"))
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128), default="")
    floor: Mapped[int] = mapped_column(Integer, default=1)
    node_type: Mapped[str] = mapped_column(String(32), default="")

    building: Mapped["IndoorBuilding"] = relationship(back_populates="nodes")


class IndoorEdge(Base):
    __tablename__ = "indoor_edges"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    building_id: Mapped[int] = mapped_column(ForeignKey("indoor_buildings.id"))
    source_code: Mapped[str] = mapped_column(String(64), index=True)
    target_code: Mapped[str] = mapped_column(String(64), index=True)
    distance: Mapped[float] = mapped_column(Float, default=0.0)
    kind: Mapped[str] = mapped_column(String(32), default="walk")
    wait_seconds: Mapped[float] = mapped_column(Float, default=0.0)
    bidirectional: Mapped[bool] = mapped_column(Boolean, default=True)

    building: Mapped["IndoorBuilding"] = relationship(back_populates="edges")
