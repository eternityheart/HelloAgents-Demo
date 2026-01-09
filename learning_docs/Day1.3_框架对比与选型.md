# Day 1.3: 框架对比与选型 🔍

> **今日目标**: 理解主流 Agent 框架的区别，掌握 HelloAgents 的架构优势
> **完成状态**: ✅ 已完成

---

## 📖 Part 1: 为什么需要框架？

### 纯 Function Calling 的问题

```
用户: "规划北京3天行程"

纯 Function Calling 的困境:
1. 查景点 → 返回10个景点
2. 查天气 → 发现第2天下雨
3. 问题: 要不要重新调整？LLM 可能忘了之前的景点...
4. 也不知道先查酒店还是先订餐厅...
```

**没有框架 = 没有"记忆"和"流程控制"**

### 框架解决的三大问题

| 问题 | 没框架 | 有框架 |
|------|--------|--------|
| 状态管理 | LLM 容易"失忆" | 框架帮你记住上下文 |
| 流程控制 | 工具调用顺序混乱 | 定义清晰的执行流程 |
| 错误处理 | API 失败就崩了 | 自动重试、回退机制 |

---

## 📊 Part 2: 三大框架对比

### 🎭 交通工具比喻

| 框架 | 比喻 | 特点 |
|------|------|------|
| HelloAgents | 🚗 自驾 | 灵活，中央调度 |
| LangGraph | 🚄 高铁 | 结构化，状态机 |
| CrewAI | 🚐 拼车 | 多角色平等协作 |

### 📝 代码风格对比

**HelloAgents (我们选的)**:
```python
orchestrator = Orchestrator()
result = orchestrator.plan("北京天气怎么样？")
# 简洁！Orchestrator 自动分析意图、派遣 Worker
```

**LangGraph**:
```python
graph = StateGraph()
graph.add_node("parse", parse_node)
graph.add_node("weather", weather_node)
graph.add_edge("parse", "weather")
app = graph.compile()
result = app.invoke({"query": "..."})
```

**CrewAI**:
```python
expert = Agent(role="气象专家", goal="...")
task = Task(description="查天气", agent=expert)
crew = Crew(agents=[expert], tasks=[task])
result = crew.kickoff()
```

### 📈 特性对比表

| 特点 | HelloAgents | LangGraph | CrewAI |
|------|-------------|-----------|--------|
| 中央调度者 | ✅ Orchestrator | ✅ Graph Router | ❌ 平等协作 |
| 专家分工 | ✅ Workers | ✅ Nodes | ✅ Agents |
| 流程灵活度 | 高 | 中（状态机） | 高 |
| 学习曲线 | 低 | 中 | 低 |
| 适合场景 | 通用任务 | 复杂流程 | 角色扮演 |

---

## 🔧 Part 3: HelloAgents 架构实战

### 架构图

```
        ┌─────────────────────────┐
        │      Orchestrator       │
        │   (LLM 意图分析器)       │
        └───────────┬─────────────┘
                    │ 返回 JSON 决策
     ┌──────────────┼──────────────┐
     ▼              ▼              ▼
┌─────────┐  ┌─────────────┐  ┌──────────┐
│  Scout  │  │ Meteorologist│  │Concierge │
│ 景点专员 │  │   天气专员   │  │ 酒店专员  │
└─────────┘  └─────────────┘  └──────────┘
```

### 核心代码位置

| 组件 | 文件 | 行号 |
|------|------|------|
| ScoutWorker | day1_3_orchestrator_demo.py | 30-46 |
| MeteorologistWorker | day1_3_orchestrator_demo.py | 49-63 |
| Orchestrator.analyze_intent | day1_3_orchestrator_demo.py | 78-105 |

### 意图分析 Prompt

```python
"""你是一个意图分析器。根据用户输入，判断需要哪些专家。
返回 JSON 格式，包含:
- city: 城市名
- needs_spots: 是否需要景点
- needs_weather: 是否需要天气
"""
```

---

## 🧪 测试验证结果

| 测试 | 输入 | 意图解析 | Workers | 结果 |
|------|------|----------|---------|------|
| 1 | "北京有什么好玩的？" | needs_spots: true | Scout | ✅ |
| 2 | "上海天气怎么样？" | needs_weather: true | Meteorologist | ✅ |
| 3 | "去广州，景点+天气" | 两个都true | Scout + Meteorologist | ✅ |

---

## 🎓 面试话术

### Q: 为什么选择 HelloAgents 而不是其他框架？

> "我选择 Orchestrator-Workers 模式因为：
> 1. **可控性高** - 中央调度器明确控制任务分配
> 2. **调试简单** - 问题出在哪个 Worker 一目了然
> 3. **灵活度高** - 不受固定状态机约束
> 4. **渐进式学习** - 先理解基本原理，再扩展到复杂框架"

### Q: Orchestrator 如何决定调用哪个 Worker？

> "我使用 LLM 做意图分析，返回结构化 JSON。这比硬编码 if-else 更灵活，能处理各种表达方式，比如'北京好玩吗'和'北京有什么景点'都能识别为景点查询。"

---

## ✅ 学习检查清单

- [x] 理解为什么需要框架（状态/流程/错误处理）
- [x] 了解三大框架的区别和适用场景
- [x] 理解 HelloAgents Orchestrator-Workers 架构
- [x] 理解 LLM 意图分析 → JSON → Worker 派遣流程
- [x] 能向面试官解释框架选型理由

---

## 📁 代码文件

| 文件 | 用途 |
|------|------|
| day1_3_orchestrator_demo.py | Orchestrator-Workers 完整演示 |

---

## 🚀 下一步

**Phase 2: 基础设施搭建** - 连接真实 API（高德地图）
