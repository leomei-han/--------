# API

## 认证

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/auth/logout`
- `GET /api/auth/demo-accounts`
- `GET /api/auth/favorites`
- `POST /api/auth/favorites/destinations`
- `POST /api/auth/favorites/routes`

## 目的地

- `GET /api/destinations`
- `GET /api/destinations/featured`
- `POST /api/destinations/recommend`
- `POST /api/destinations/search`

## 路线

- `POST /api/routes/single`
- `POST /api/routes/multi`

## 地图场景

- `GET /api/map/scenes`
- `GET /api/map/scenes/{scene_name}`

## 设施 / 美食 / 日记

- `GET /api/facilities/nearby`
- `GET /api/foods`
- `GET /api/diaries`
- `GET /api/diaries/{diary_id}`
- `POST /api/diaries/search`
- `POST /api/diaries/{diary_id}/view`
- `POST /api/diaries/{diary_id}/rate`
- `POST /api/diaries/compress`
- `POST /api/diaries/decompress`

## 辅助与管理

- `GET /api/agents`
- `GET /api/admin/import/status`
