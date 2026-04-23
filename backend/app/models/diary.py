from __future__ import annotations

from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Diary(Base):
    __tablename__ = "diaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(256), index=True)
    destination_name: Mapped[str] = mapped_column(String(128), index=True)
    content: Mapped[str] = mapped_column(Text)
    views: Mapped[int] = mapped_column(Integer, default=0)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    media_urls: Mapped[str] = mapped_column(Text, default="[]")
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    author_name: Mapped[str] = mapped_column(String(128), default="")
    created_at: Mapped[str] = mapped_column(String(32), default="")

    ratings: Mapped[list[DiaryRating]] = relationship(
        "DiaryRating", back_populates="diary", lazy="selectin"
    )


class DiaryRating(Base):
    __tablename__ = "diary_ratings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    diary_id: Mapped[int] = mapped_column(Integer, ForeignKey("diaries.id"), index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    score: Mapped[float] = mapped_column(Float)
    updated_at: Mapped[str] = mapped_column(String(32), default="")

    diary: Mapped[Diary] = relationship("Diary", back_populates="ratings")
