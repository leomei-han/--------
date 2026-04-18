# 北京高校与景区个性化旅游系统

基于真实地理数据、课程设计算法要求和前后端分离架构实现的个性化旅游系统。项目覆盖景区/校园推荐、路线规划、附近设施查询、美食推荐、旅游日记管理与全文检索，并为课程验收准备了完整的工程目录、文档骨架和数据导入链路。

## 技术栈

- 前端：Vue 3、TypeScript、Vite、Pinia、Vue Router、Leaflet
- 后端：FastAPI、SQLAlchemy、Pydantic、Uvicorn
- 数据：PostgreSQL + PostGIS（开发期也支持 JSON 数据快照做演示）
- 算法：堆、Quickselect、Trie、倒排索引、Dijkstra、A*、Held-Karp、2-opt、Huffman

## 快速开始

### 1. 后端虚拟环境

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. 前端

```powershell
cd frontend
npm install
npm run dev
```

### 3. 真实数据抓取

```powershell
cd data_pipeline
..\backend\.venv\Scripts\python.exe scripts\fetch_osm_data.py
..\backend\.venv\Scripts\python.exe scripts\build_demo_dataset.py
```

## 目录

- `backend/`：FastAPI 服务、算法实现、数据模型、测试
- `frontend/`：Vue 前端、地图与演示页面
- `data_pipeline/`：真实数据抓取与清洗脚本
- `datasets/`：原始快照、清洗结果和演示数据
- `docs/`：课程报告所需文档骨架
- `infra/`：数据库与环境说明

## 当前状态

当前仓库已完成：

- 工程结构初始化
- 后端基础 API、算法模块与测试样例
- 前端页面骨架与 API 集成层
- 真实数据抓取脚本与演示数据构建脚本
- 课程设计文档模板

## 数据说明

- `datasets/raw/beijing_destinations_osm.json`、`datasets/raw/bupt_scene.json`、`datasets/raw/summer_palace_scene.json` 等来源于 OpenStreetMap / Overpass 抓取结果
- `datasets/prod/destinations.json`、`facilities.json`、`foods.json` 基于真实公开地理点位构建
- `datasets/prod/users.json`、`diaries.json` 为课程演示联调用种子数据，不宣称为真实公开用户数据

后续可以继续补齐：

- PostGIS 实库接入与 Alembic 迁移
- 更大规模真实数据清洗
- 地图精细化导航与验收演示素材
