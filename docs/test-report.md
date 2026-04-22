# Test Report (2026-04-19)

## 1. 测试范围

- 算法层：Top-K、Quickselect、Hash/Trie/倒排索引、Dijkstra、Held-Karp、2-opt、Huffman、室内导航最短路、AIGC 分镜生成
- 服务与接口层：推荐、搜索、路线、室内导航、设施、美食、日记发布/检索/详情/浏览/评分/压缩/解压/AIGC 动画
- 前端构建层：Vue + TypeScript 编译与 Vite 打包

## 2. 执行命令与结果

### 2.1 后端测试

命令：

```bash
cd backend
/home/mr/projects/--------/.venv/bin/python -m pytest tests/test_algorithms.py tests/test_api.py -q
```

结果：

- `32 passed in 0.53s`

### 2.2 前端构建

命令：

```bash
cd frontend
npm run build
```

结果：

- `vue-tsc --noEmit` 通过
- `vite build` 通过

## 3. 关键新增用例

- `test_diary_view_and_rate_interaction_flow`
- `test_diary_compress_and_decompress_roundtrip`
- `test_compression_service_returns_ratio_metrics`
- `test_search_service_fuzzy_results_are_ranked_by_heat_and_rating`
- `test_indoor_route_cross_floor_contains_elevator_instruction`
- `test_indoor_route_wheelchair_mode_avoids_stairs`
- `test_diary_aigc_animation_endpoint_returns_storyboard`

## 4. 数据隔离说明

- API 测试通过 `app.dependency_overrides[get_repository]` + `tmp_path` 拷贝数据目录运行，避免污染 `datasets/prod`。

## 5. 结论

- 当前版本通过核心后端测试与前端构建验证，可作为课堂验收候选版本。
