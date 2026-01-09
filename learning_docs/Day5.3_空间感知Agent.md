# Day 5.3: 空间感知 Agent (Spatial Scout) 🧠

> **今日目标**: 打造一个懂"附近"的 AI
> **核心成果**: `src/phase5/spatial_agent.py`

---

## 📖 Part 1: 什么是"空间感知"？

当用户说："**附近的**加油站"时，这句话其实隐含了一个变量：`user_location`。
普通的 Scout Agent (Phase 4) 是瞎子，它只能接受 `city="北京"`。

空间感知 Agent (Phase 5) 进化了：
1. **Tool Definition**: 增加了 `user_lat`, `user_lon` 参数。
2. **Logic Hook**: 在调用 API 后，不仅仅返回 Data，而是调用 `process_pois(data, user_lat, user_lon)`。

---

## 🔧 Part 2: 实战代码变化

### 1. 工具定义的升级
```python
@mcp.tool
def search_nearby(keyword, user_lat, user_lon, ...):
    ...
```
LLM 会根据 Prompt 自动提取用户的坐标（在未来的 Phase 7 前端集成中，这个坐标通常由浏览器 JS 获取并注入到 Prompt Context 中）。

### 2. Pipeline 模式
我们的代码越来越像一条流水线：
`Prompt` -> `Orchestrator` -> `Spatial Agent` -> `Amap API` -> `Data Processor` -> `Final Response`

- **Scout**: 负责"找" (Recall)
- **Data Processor**: 负责"算" (Rank)

---

## 🧪 验证结果

运行 `src/phase5/test_spatial.py`：

**Case: 寻找天安门附近的厕所**
> 1. 南池子街公共厕所 | 📏 510m
> 2. 公共厕所 | 📏 780m
> ...

AI 成功帮你找到了最近的坑位！(非常实用)

---

## 🎓 面试话术

### Q: 你的 Agent 如何实现"附近推荐"？
> "我在 Agent 内部实现了一个简单的 **RAG (Retrieval-Augmented Generation)** 变体。
> 1. **Retrieval**: 利用高德 API 的 `place/text` 接口，配合 `citylimit` 参数，先召回候选 POI 集合。
> 2. **Rerank**: 在本地利用 Haversine 公式计算每个候选点到 `user_location` 的球面距离，并进行二次排序。
> 这样的两阶段处理，既利用了搜索引擎的广度，又保证了结果对用户的空间相关性。"

---

## ✅ 学习检查清单

- [x] 理解如何将 User Context (Location) 传递给 Tool
- [x] 实现 "API 召回 + 本地重排" 模式
- [x] 完成 Phase 5 的所有地理空间任务

---

## 🚀 Phase 5 结项

现在我们的 Agent 已经具备了：
- **手**: API 调用能力
- **脑**: 意图识别与记忆
- **眼**: 空间感知能力

我们已经跑通了后端的所有核心逻辑。
接下来的 Phase 6，我们要把这些代码封装成 **Web 服务 (FastAPI)**，为前端界面的接入做准备！
