# Day 4.1: Scout Agent (侦察兵) 🔭

> **今日目标**: 迈出"微服务化"的第一步，用 FastMCP 封装 POI 搜索
> **核心成果**: `src/phase4/scout_agent.py`

---

## 📖 Part 1: 普通函数 vs Expert Agent

### 以前 (Phase 3)
```python
# tools.py
def search_poi(city, keyword):
    ...
```
这只是一个**死**的代码块，只能被 Python 代码 `import` 调用。

### 现在 (Phase 4)
```python
# scout_agent.py
@mcp.tool()
def search_poi(city, keyword):
    ...

mcp.run()
```
这就是一个**活**的 Agent（或者叫 MCP Server）。
- 它是一个独立的进程
- 它通过标准协议 (JSON-RPC) 通信
- **任何**支持 MCP 的客户端 (Claude Desktop, Cursor, 或我们自己的 Orchestrator) 都能连接它，而不需要知道它是用 Python 写的。

---

## 🔧 Part 2: 实战代码剖析

### 1. 也是 "Hello World"
我们使用了 `FastMCP` 库，它极大地简化了 MCP Server 的编写。
```python
from fastmcp import FastMCP

# 创建一个 Server 实例
mcp = FastMCP("Scout Agent")
```

### 2. @mcp.tool 装饰器
这是核心魔法。加上这个装饰器，普通函数就变成了 "Tool Resource"。
客户端连接后，会自动发现这个工具及其参数描述。
```python
@mcp.tool(description="搜索POI...")
def search_poi(...)
```

### 3. "逻辑分离" 技巧
在开发中，为了方便测试（不启动 Server 也能跑），我把业务逻辑拆分成了 `_search_poi_logic` 私有函数。
这是工程化中的常见 Pattern：**接口层 (Wrapper) 与 逻辑层 (Core Logic) 分离**。

---

## 🧪 验证结果

运行 `src/phase4/test_scout_direct.py`：
> 1. 搜索 '北京 故宫 (景点)'...
> ✅ 找到: 天坛公园, 地坛公园...

这证明我们的核心搜索逻辑移植成功。
只要运行 `python scout_agent.py`，它就会变成一个监听 Server（虽然在终端里看不到可以直接交互的界面，因为它在等待 Client 连接）。

---

## 🎓 面试话术

### Q: 为什么要用 MCP 而不是直接写 API？
> "直接写 HTTP API (FastAPI) 当然可以，但 MCP 提供了一套**针对 LLM 优化的协议标准**。
> 使用 MCP，我不需要写复杂的 OpenAPI 文档，LLM Client 就能自动发现工具、理解参数结构。
> 它是 'AI Native' 的微服务协议。"

### Q: 你的 Scout Agent 是怎么部署的？
> "目前作为本地进程运行 (stdio 模式)。Orchestrator 通过子进程方式启动它。
> 在生产环境中，可以将 FastMCP 部署为 SSE (Server-Sent Events) 服务，支持远程调用。"

---

## ✅ 学习检查清单

- [x] 理解 MCP Server 的概念
- [x] 使用 `FastMCP` 创建第一个 Agent
- [x] 掌握 `@mcp.tool` 装饰器
- [x] 移植并验证 POI 搜索逻辑

---

## 🚀 下一步

**Day 4.2: Meteorologist Agent (气象员)**
Scout 只是简单的搜索。
气象员稍微复杂一点，我们要把天气查询也封装通过，并且强化一下**错误处理**规范。
