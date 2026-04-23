from __future__ import annotations

from sqlalchemy import ForeignKey, String, Text, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(128), default="")
    interests: Mapped[str] = mapped_column(String(256), default="")
    password_hash: Mapped[str] = mapped_column(String(256), default="")
    created_at: Mapped[str] = mapped_column(String(32), default="")
    last_login_at: Mapped[str] = mapped_column(String(32), default="")

    sessions: Mapped[list[Session]] = relationship("Session", back_populates="user")
    favorite_destinations: Mapped[list[UserFavoriteDestination]] = relationship(
        "UserFavoriteDestination", back_populates="user"
    )
    favorite_routes: Mapped[list[UserFavoriteRoute]] = relationship(
        "UserFavoriteRoute", back_populates="user"
    )


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    created_at: Mapped[str] = mapped_column(String(32), default="")

    user: Mapped[User] = relationship("User", back_populates="sessions")


class UserFavoriteDestination(Base):
    __tablename__ = "user_favorite_destinations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    destination_source_id: Mapped[str] = mapped_column(String(128))

    user: Mapped[User] = relationship("User", back_populates="favorite_destinations")


class UserFavoriteRoute(Base):
    __tablename__ = "user_favorite_routes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    scene_name: Mapped[str] = mapped_column(String(128), default="")
    strategy: Mapped[str] = mapped_column(String(32), default="")
    transport_mode: Mapped[str] = mapped_column(String(32), default="")
    path_codes: Mapped[str] = mapped_column(Text, default="")
    path_names: Mapped[str] = mapped_column(Text, default="")
    total_distance_m: Mapped[float] = mapped_column(Float, default=0.0)
    estimated_minutes: Mapped[float] = mapped_column(Float, default=0.0)
    explanation: Mapped[str] = mapped_column(Text, default="")
    saved_at: Mapped[str] = mapped_column(String(32), default="")

    user: Mapped[User] = relationship("User", back_populates="favorite_routes")
