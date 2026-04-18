from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Diary(Base):
    __tablename__ = "diaries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    destination_name: Mapped[str] = mapped_column(String(128), index=True)
    title: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    content: Mapped[str] = mapped_column(Text)
    media_urls: Mapped[str] = mapped_column(Text, default="")
    views: Mapped[int] = mapped_column(Integer, default=0)
    rating: Mapped[float] = mapped_column(Float, default=0.0)


class DiaryRating(Base):
    __tablename__ = "diary_ratings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    diary_id: Mapped[int] = mapped_column(ForeignKey("diaries.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    score: Mapped[float] = mapped_column(Float)
