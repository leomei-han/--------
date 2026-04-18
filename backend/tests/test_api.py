from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_destinations_endpoint_returns_real_dataset():
    response = client.get("/api/destinations")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 200
    assert any(item["name"] == "北京邮电大学" for item in data)


def test_featured_destinations_include_scenic_and_shopping():
    response = client.get("/api/destinations/featured")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 8
    categories = {item["category"] for item in data}
    assert "scenic" in categories
    assert "shopping" in categories
    assert all(item["rating"] is not None for item in data)
    assert all(item["source_url"] for item in data)


def test_single_route_endpoint_returns_path():
    response = client.post(
        "/api/routes/single",
        json={
            "scene_name": "BUPT_Main_Campus",
            "start_code": "BUPT_GATE",
            "end_code": "BUPT_LIB",
            "strategy": "distance",
            "transport_mode": "walk",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["path_codes"]
    assert payload["path_names"]
    assert payload["estimated_minutes"] >= 0
    assert "alternatives" in payload


def test_nearby_facilities_endpoint_returns_graph_distance():
    response = client.get(
        "/api/facilities/nearby",
        params={"scene_name": "BUPT_Main_Campus", "origin_code": "BUPT_GATE"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data
    assert "graph_distance" in data[0]


def test_foods_endpoint_returns_structured_items():
    response = client.get("/api/foods")
    assert response.status_code == 200
    payload = response.json()
    assert payload["items"]
    assert payload["items"][0]["rating"] is not None


def test_diary_search_and_detail_return_structured_payload():
    search_response = client.post("/api/diaries/search", json={"query": "故宫"})
    assert search_response.status_code == 200
    payload = search_response.json()
    assert "items" in payload
    diary_id = payload["items"][0]["id"]
    detail_response = client.get(f"/api/diaries/{diary_id}")
    assert detail_response.status_code == 200
    assert detail_response.json()["content"]


def test_auth_register_me_favorite_and_logout_flow():
    username = f"test_{uuid4().hex[:8]}"
    register_response = client.post(
        "/api/auth/register",
        json={"username": username, "password": "secret123", "display_name": "测试用户"},
    )
    assert register_response.status_code == 200
    payload = register_response.json()
    token = payload["token"]
    headers = {"Authorization": f"Bearer {token}"}

    me_response = client.get("/api/auth/me", headers=headers)
    assert me_response.status_code == 200
    assert me_response.json()["user"]["username"] == username

    favorite_response = client.post(
        "/api/auth/favorites/destinations",
        json={"source_id": "featured-5"},
        headers=headers,
    )
    assert favorite_response.status_code == 200
    assert "featured-5" in favorite_response.json()["user"]["favorite_destination_ids"]

    route_response = client.post(
        "/api/auth/favorites/routes",
        json={
            "scene_name": "BUPT_Main_Campus",
            "strategy": "distance",
            "transport_mode": "walk",
            "path_codes": ["BUPT_GATE", "BUPT_LIB"],
            "path_names": ["南门", "图书馆"],
            "total_distance_m": 100,
            "estimated_minutes": 2.1,
            "explanation": "测试路线",
        },
        headers=headers,
    )
    assert route_response.status_code == 200
    assert route_response.json()["user"]["favorite_route_snapshots"]

    logout_response = client.post("/api/auth/logout", headers=headers)
    assert logout_response.status_code == 200


def test_create_diary_requires_auth_and_persists():
    login_response = client.post("/api/auth/login", json={"username": "demo_user_1", "password": "demo123"})
    assert login_response.status_code == 200
    token = login_response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_response = client.post(
        "/api/diaries",
        json={
            "destination_name": "故宫博物院",
            "title": "测试发布日记",
            "content": "这是一篇用于接口测试的新日记。",
            "cover_image_url": "/media/destinations/destination-01.svg",
            "media_urls": ["/media/destinations/destination-01.svg"],
        },
        headers=headers,
    )
    assert create_response.status_code == 200
    assert create_response.json()["author_name"]
