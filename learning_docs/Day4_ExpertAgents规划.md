# Phase 4: 专家 Agent 开发 (Expert Agents) 👷

> **本阶段目标**: 从"单体应用"向"微服务架构"演进。我们将使用 **FastMCP** 将之前的工具函数封装为标准的 MCP 服务器。
> **关键词**: `FastMCP`, `Microservices`, `Specialized Agents`

---

## 📅 Day 4 学习路线图

### Day 4.1: Scout Agent (侦察兵) 🔭
- **目标**: 将 POI 搜索功能封装为独立服务
- **核心概念**:
    - FastMCP 基础用法
    - `@mcp.tool` 装饰器
    - 独立运行与调试

### Day 4.2: Meteorologist Agent (气象员) 🌤️
- **目标**: 将天气查询功能封装为独立服务
- **核心概念**:
    - JSON 参数校验 (Pydantic 集成)
    - 错误处理标准
    - 多工具注册

### Day 4.3: Concierge Agent (礼宾员) 🛎️ && 集成
- **目标**: Orchestrator 如何调用这些独立的 Agent
- **核心概念**:
    - Client 连接 Server
    - 动态工具加载
    - 本地 MCP 服务通信

---

## 🏗️ 架构演进

**Before (Phase 3)**:
```python
# Orchestrator 直接 import 工具函数
from tools import get_weather, search_poi
```

**After (Phase 4)**:
```python
# Orchestrator 通过 MCP 协议连接独立进程
class Orchestrator:
    def connect_servers(self):
        self.weather_client.connect("stdio:python weather_agent.py")
        self.scout_client.connect("stdio:python scout_agent.py")
```

---

## 📝 交付物清单

1. `src/phase4/scout_agent.py` (基于 FastMCP)
2. `src/phase4/weather_agent.py` (基于 FastMCP)
3. `src/phase4/main.py` (集成测试)

---

## 🚀 开始第一步: Day 4.1 Scout Agent

我们将把 `search_poi` 函数改造为一个标准的 MCP Server。
这样不仅仅是 Python，甚至其他语言的 Agent (如 Claude Desktop) 也能直接调用它！
