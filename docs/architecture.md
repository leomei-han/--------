# Architecture

前端采用 Vue 3 + TypeScript，后端采用 FastAPI，数据库目标为 PostgreSQL + PostGIS。当前仓库同时保留 JSON 数据快照路径，便于在没有数据库时完成演示、测试和算法联调。

## 分层

- 展示层：`frontend/`
- 接口层：`backend/app/api/`
- 业务服务层：`backend/app/services/`
- 算法层：`backend/app/algorithms/`
- 数据层：`backend/app/models/` 与 `datasets/prod/`
- 数据管线：`data_pipeline/scripts/`

## 数据真实性边界

- 公开地理点位数据来自 OSM / Overpass
- 校园与景区样板场景中的节点、设施名称与坐标优先来自真实抓取结果
- 用户、日记等交互数据目前为演示种子数据，便于系统联调与课堂验收展示
