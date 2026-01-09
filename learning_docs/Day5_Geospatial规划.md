# Phase 5: 地理空间数据处理 (Geospatial Data) 🗺️

> **本阶段目标**: 让 Agent 具备"空间感知"能力。不仅知道地点的名字，还能计算距离、筛选范围、理解坐标系。
> **关键词**: `Haversine Formula`, `GCJ-02`, `Data Cleaning`

---

## 📅 Day 5 学习路线图

### Day 5.1: 坐标系与距离计算 📏
- **目标**: 理解为什么地图坐标会有偏差，并实现距离计算
- **核心概念**:
    - WGS-84 (国际标准) vs GCJ-02 (火星坐标)
    - Haversine 公式 (计算球面距离)
    - Python `math` 模块应用

### Day 5.2: 数据清洗与排序 🧹
- **目标**: 处理 API 返回的原始数据，按距离排序
- **核心概念**:
    - `lambda` 排序
    - 数据结构化 (Dict -> Object)
    - 过滤脏数据 (无坐标的 POI)

### Day 5.3: 空间感知 Agent 🧠
- **目标**: 升级 Scout Agent，支持 "搜索我附近的..."
- **核心概念**:
    - 在 Tool 中增加 `user_location` 参数
    - 实现 "Near Me" 语义理解

---

## 🏗️ 技能树演进

**Before (Phase 4)**:
Agent 只能返回一堆文字列表，不知道哪个离用户最近。

**After (Phase 5)**:
Agent 能回答："离你最近的是 A餐厅 (500米)，稍微远点有 B餐厅 (1.2公里)。"

---

## 📝 交付物清单

1. `src/phase5/geo_utils.py` (坐标转换与距离计算工具库)
2. `src/phase5/data_processor.py` (数据清洗管道)
3. `src/phase5/spatial_agent.py` (具备空间感的 Agent)

---

## 🚀 开始第一步: Day 5.1 坐标系

在中国开发地图应用，避不开 **GCJ-02 (火星坐标系)**。
高德 API 返回的是 GCJ-02，但有些国际库用的是 WGS-84。
虽然对于简单的距离排序影响不大，但作为专业工程师，必须理解它们的区别。
