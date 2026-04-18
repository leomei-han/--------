# Schema

## 核心实体

- `users`
- `destinations`
- `scenes`
- `buildings`
- `facilities`
- `roads`
- `edges`
- `food_pois`
- `diaries`
- `diary_ratings`

## 关键关系

- 一个 `destination` 可对应多个 `scene`
- 一个 `scene` 可挂接多个建筑、设施和边
- `diary` 由用户创建，并与目的地名称关联
