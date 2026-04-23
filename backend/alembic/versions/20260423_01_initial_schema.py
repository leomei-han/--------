"""initial schema

Revision ID: 20260423_01
Revises:
Create Date: 2026-04-23 00:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260423_01"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "destinations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("source_id", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("city", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("category", sa.String(length=32), nullable=False),
        sa.Column("district", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("address", sa.String(length=256), nullable=False, server_default=""),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column("heat", sa.Float(), nullable=True),
        sa.Column("heat_metric", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("tags", sa.String(length=512), nullable=False, server_default=""),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("image_url", sa.String(length=256), nullable=False, server_default=""),
        sa.Column("image_source_name", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("image_source_url", sa.String(length=256), nullable=False, server_default=""),
        sa.Column("source_name", sa.String(length=128), nullable=True),
        sa.Column("source_url", sa.String(length=256), nullable=True),
        sa.Column("fetched_date", sa.String(length=32), nullable=True),
        sa.Column("is_featured", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("rating_source_name", sa.String(length=128), nullable=True),
        sa.Column("rating_source_url", sa.String(length=256), nullable=True),
        sa.Column("heat_source_name", sa.String(length=128), nullable=True),
        sa.Column("heat_source_url", sa.String(length=256), nullable=True),
    )
    op.create_index("ix_destinations_source_id", "destinations", ["source_id"], unique=True)
    op.create_index("ix_destinations_name", "destinations", ["name"], unique=False)
    op.create_index("ix_destinations_category", "destinations", ["category"], unique=False)

    op.create_table(
        "scenes",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("label", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("city", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("supports_routing", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_scenes_name", "scenes", ["name"], unique=True)

    op.create_table(
        "scene_nodes",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("scene_id", sa.Integer(), sa.ForeignKey("scenes.id"), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
    )
    op.create_index("ix_scene_nodes_code", "scene_nodes", ["code"], unique=True)

    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("scene_id", sa.Integer(), sa.ForeignKey("scenes.id"), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("building_type", sa.String(length=64), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
    )
    op.create_index("ix_buildings_code", "buildings", ["code"], unique=True)

    op.create_table(
        "facilities",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("scene_id", sa.Integer(), sa.ForeignKey("scenes.id"), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("facility_type", sa.String(length=64), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
    )
    op.create_index("ix_facilities_code", "facilities", ["code"], unique=True)
    op.create_index("ix_facilities_facility_type", "facilities", ["facility_type"], unique=False)

    op.create_table(
        "edges",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("scene_id", sa.Integer(), sa.ForeignKey("scenes.id"), nullable=False),
        sa.Column("source_code", sa.String(length=64), nullable=False),
        sa.Column("target_code", sa.String(length=64), nullable=False),
        sa.Column("distance", sa.Float(), nullable=False),
        sa.Column("congestion", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("walk_speed", sa.Float(), nullable=False, server_default="1.1"),
        sa.Column("bike_speed", sa.Float(), nullable=False, server_default="3.5"),
        sa.Column("shuttle_speed", sa.Float(), nullable=False, server_default="4.8"),
        sa.Column("allowed_modes", sa.String(length=128), nullable=False, server_default="walk"),
    )
    op.create_index("ix_edges_source_code", "edges", ["source_code"], unique=False)
    op.create_index("ix_edges_target_code", "edges", ["target_code"], unique=False)

    op.create_table(
        "foods",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("source_id", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("city", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("destination_name", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("cuisine", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("venue_name", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("latitude", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("longitude", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column("heat", sa.Float(), nullable=True),
        sa.Column("heat_metric", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("source_name", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("source_url", sa.String(length=256), nullable=False, server_default=""),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("image_url", sa.String(length=256), nullable=False, server_default=""),
        sa.Column("image_source_name", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("image_source_url", sa.String(length=256), nullable=False, server_default=""),
        sa.Column("fetched_date", sa.String(length=32), nullable=False, server_default=""),
    )
    op.create_index("ix_foods_source_id", "foods", ["source_id"], unique=True)
    op.create_index("ix_foods_name", "foods", ["name"], unique=False)
    op.create_index("ix_foods_cuisine", "foods", ["cuisine"], unique=False)

    op.create_table(
        "indoor_buildings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("building_code", sa.String(length=64), nullable=False),
        sa.Column("building_name", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("scene_name", sa.String(length=128), nullable=False, server_default=""),
    )
    op.create_index("ix_indoor_buildings_building_code", "indoor_buildings", ["building_code"], unique=True)

    op.create_table(
        "indoor_nodes",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("building_id", sa.Integer(), sa.ForeignKey("indoor_buildings.id"), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("floor", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("node_type", sa.String(length=32), nullable=False, server_default=""),
    )
    op.create_index("ix_indoor_nodes_code", "indoor_nodes", ["code"], unique=True)

    op.create_table(
        "indoor_edges",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("building_id", sa.Integer(), sa.ForeignKey("indoor_buildings.id"), nullable=False),
        sa.Column("source_code", sa.String(length=64), nullable=False),
        sa.Column("target_code", sa.String(length=64), nullable=False),
        sa.Column("distance", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("kind", sa.String(length=32), nullable=False, server_default="walk"),
        sa.Column("wait_seconds", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("bidirectional", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_indoor_edges_source_code", "indoor_edges", ["source_code"], unique=False)
    op.create_index("ix_indoor_edges_target_code", "indoor_edges", ["target_code"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("display_name", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("interests", sa.String(length=256), nullable=False, server_default=""),
        sa.Column("password_hash", sa.String(length=256), nullable=False, server_default=""),
        sa.Column("created_at", sa.String(length=32), nullable=False, server_default=""),
        sa.Column("last_login_at", sa.String(length=32), nullable=False, server_default=""),
    )
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "sessions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("token", sa.String(length=128), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.String(length=32), nullable=False, server_default=""),
    )
    op.create_index("ix_sessions_token", "sessions", ["token"], unique=True)

    op.create_table(
        "user_favorite_destinations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("destination_source_id", sa.String(length=128), nullable=False),
    )
    op.create_index(
        "ix_user_favorite_destinations_user_id",
        "user_favorite_destinations",
        ["user_id"],
        unique=False,
    )

    op.create_table(
        "user_favorite_routes",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("scene_name", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("strategy", sa.String(length=32), nullable=False, server_default=""),
        sa.Column("transport_mode", sa.String(length=32), nullable=False, server_default=""),
        sa.Column("path_codes", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("path_names", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("total_distance_m", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("estimated_minutes", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("explanation", sa.Text(), nullable=False, server_default=""),
        sa.Column("saved_at", sa.String(length=32), nullable=False, server_default=""),
    )
    op.create_index("ix_user_favorite_routes_user_id", "user_favorite_routes", ["user_id"], unique=False)

    op.create_table(
        "diaries",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("destination_name", sa.String(length=128), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("views", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rating", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("media_urls", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("author_name", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("created_at", sa.String(length=32), nullable=False, server_default=""),
    )
    op.create_index("ix_diaries_title", "diaries", ["title"], unique=False)
    op.create_index("ix_diaries_destination_name", "diaries", ["destination_name"], unique=False)

    op.create_table(
        "diary_ratings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("diary_id", sa.Integer(), sa.ForeignKey("diaries.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("updated_at", sa.String(length=32), nullable=False, server_default=""),
    )
    op.create_index("ix_diary_ratings_diary_id", "diary_ratings", ["diary_id"], unique=False)
    op.create_index("ix_diary_ratings_user_id", "diary_ratings", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_diary_ratings_user_id", table_name="diary_ratings")
    op.drop_index("ix_diary_ratings_diary_id", table_name="diary_ratings")
    op.drop_table("diary_ratings")

    op.drop_index("ix_diaries_destination_name", table_name="diaries")
    op.drop_index("ix_diaries_title", table_name="diaries")
    op.drop_table("diaries")

    op.drop_index("ix_user_favorite_routes_user_id", table_name="user_favorite_routes")
    op.drop_table("user_favorite_routes")

    op.drop_index("ix_user_favorite_destinations_user_id", table_name="user_favorite_destinations")
    op.drop_table("user_favorite_destinations")

    op.drop_index("ix_sessions_token", table_name="sessions")
    op.drop_table("sessions")

    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")

    op.drop_index("ix_indoor_edges_target_code", table_name="indoor_edges")
    op.drop_index("ix_indoor_edges_source_code", table_name="indoor_edges")
    op.drop_table("indoor_edges")

    op.drop_index("ix_indoor_nodes_code", table_name="indoor_nodes")
    op.drop_table("indoor_nodes")

    op.drop_index("ix_indoor_buildings_building_code", table_name="indoor_buildings")
    op.drop_table("indoor_buildings")

    op.drop_index("ix_foods_cuisine", table_name="foods")
    op.drop_index("ix_foods_name", table_name="foods")
    op.drop_index("ix_foods_source_id", table_name="foods")
    op.drop_table("foods")

    op.drop_index("ix_edges_target_code", table_name="edges")
    op.drop_index("ix_edges_source_code", table_name="edges")
    op.drop_table("edges")

    op.drop_index("ix_facilities_facility_type", table_name="facilities")
    op.drop_index("ix_facilities_code", table_name="facilities")
    op.drop_table("facilities")

    op.drop_index("ix_buildings_code", table_name="buildings")
    op.drop_table("buildings")

    op.drop_index("ix_scene_nodes_code", table_name="scene_nodes")
    op.drop_table("scene_nodes")

    op.drop_index("ix_scenes_name", table_name="scenes")
    op.drop_table("scenes")

    op.drop_index("ix_destinations_category", table_name="destinations")
    op.drop_index("ix_destinations_name", table_name="destinations")
    op.drop_index("ix_destinations_source_id", table_name="destinations")
    op.drop_table("destinations")
