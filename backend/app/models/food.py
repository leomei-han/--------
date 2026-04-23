from sqlalchemy import Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Food(Base):
    __tablename__ = "foods"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(128), index=True)
    city: Mapped[str] = mapped_column(String(64), default="")
    destination_name: Mapped[str] = mapped_column(String(128), default="")
    cuisine: Mapped[str] = mapped_column(String(64), index=True, default="")
    venue_name: Mapped[str] = mapped_column(String(128), default="")
    latitude: Mapped[float] = mapped_column(Float, default=0.0)
    longitude: Mapped[float] = mapped_column(Float, default=0.0)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    heat: Mapped[float | None] = mapped_column(Float, nullable=True)
    heat_metric: Mapped[str] = mapped_column(String(64), default="")
    source_name: Mapped[str] = mapped_column(String(128), default="")
    source_url: Mapped[str] = mapped_column(String(256), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    image_url: Mapped[str] = mapped_column(String(256), default="")
    image_source_name: Mapped[str] = mapped_column(String(128), default="")
    image_source_url: Mapped[str] = mapped_column(String(256), default="")
    fetched_date: Mapped[str] = mapped_column(String(32), default="")
