# Day 5.2: 数据清洗与排序 (Data Cleaning) 🧹

> **今日目标**: 让搜索结果更有条理，实现"按距离排序"
> **核心成果**: `src/phase5/data_processor.py`

---

## 📖 Part 1: 数据增强 (Data Enrichment)

API 返回的原始数据通常是"贫瘠"的。
比如高德 POI 结果：
```json
{ "name": "故宫", "location": "116.397,39.918" }
```
它只有坐标，没有"离我多远"这个概念。
我们需要在中间层做一步 **Enrichment**:
1. 获取 User Location
2. 计算 Distance
3. 将 Distance 注入到数据对象中 (`_distance` 字段)

---

## 🔧 Part 2: 实战代码技巧

### 1. 为什么用下划线 `_distance`?
为了区分**原始数据**和**衍生数据**。
- `name`, `address` 是 API 给的。
- `_distance` 是我们算的。
这是一个好的工程习惯，方便后续做 Data Mapping 时区分。

### 2. Python Lambda 排序
```python
# 一行代码搞定排序
enriched_pois.sort(key=lambda x: x["_distance"])
```

### 3. 友好的格式化
用户不想看经纬度，也不想看 "1023.45 meter"。
- 小于 1km -> 显示 "900m"
- 大于 1km -> 显示 "1.2km"
这些 UI 细节是提升用户体验的关键。

---

## 🧪 验证结果

运行 `src/phase5/test_data_processor.py`：

我们模拟了用户在**天安门**。
输入了三个乱序地点：北京南站(5km), 故宫(1km), 天坛(3km)。

**输出结果**:
> 1. 故宫博物院 (近) | 📏 1.0km
> 2. 天坛公园 (中) | 📏 3.0km
> 3. 北京南站 (远) | 📏 5.1km

排序完全正确！✅

---

## 🎓 面试话术

### Q: 你的 Agent 是如何处理大量搜索结果的？
> "我在中间层实现了一个 `DataProcessor`。
> 它不仅仅是透传 API 结果，而是会结合用户当前的 Context (比如位置信息) 进行 **Rerank (重排序)**。
> 具体来说，我会计算每个 POI 的 Haversine 距离，并按距离优先排序，同时过滤掉缺失坐标的脏数据，确保 LLM 拿到的 Context 是高质量的。"

---

## ✅ 学习检查清单

- [x] 理解数据增强 (Enrichment) 的概念
- [x] 掌握 Python 列表排序 (`sort key`)
- [x] 实现友好的距离显示逻辑

---

## 🚀 下一步

**Day 5.3: 空间感知 Agent**
也就是 Phase 5 的终极目标。
我们将把 `Haversine` 和 `DataProcessor` 集成到 `Scout Agent` 中。
给 `search_poi` 工具增加两个参数：`user_lat`, `user_lon`。
这样用户只要说："**附近的**加油站"，Agent 就会自动调用定位并返回排序后的结果！
