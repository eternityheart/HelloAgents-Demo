# Day 4.3: Concierge Agent (礼宾员) 🛎️

> **今日目标**: 成为真正的"指挥官"，调度多 Agent 协同工作
> **核心成果**: `src/phase4/concierge.py`

---

## 📖 Part 1: 多 Agent 架构 (The Multi-Agent Architecture)

在 Phase 3，我们的架构是 **Monolithic (单体)** 的：
`Orchestrator` -> 直接 import `tools.py`

在 Phase 4，我们进化到了 **Microservices (微服务)**：
`Concierge` (Client) -> Connects to -> `Scout Process` (Server) & `Meteorologist Process` (Server)

### 🌟 核心优势
1. **解耦**: 气象员挂了，不影响侦察兵。
2. **异构**: 侦察兵可以用 Python 写，气象员可以用 Node.js 写，只要懂 MCP 协议就行。
3. **动态**: 礼宾员不需要知道工具有哪些，连上服务的那一刻，它就"学会"了新技能 (Dynamic Tool Discovery)。

---

## 🔧 Part 2: 关键代码解析

### 1. MCP Client 标准连接
这是连接一个 MCP Server 的标准姿势：

```python
# 1. 定义子进程参数 (stdio 模式)
server_params = StdioServerParameters(command="python", args=["agent_script.py"])

# 2. 建立通道
async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # 3. 初始化并发现工具
        await session.initialize()
        tools = await session.list_tools()
```

### 2. 工具路由 (Tool Routing)
Orchestrator 维护了一张路由表：
`self.tools_map = { "search_poi": "Scout", "get_weather": "Meteorologist" }`

当 LLM 决定调用 `search_poi` 时：
1. 查找路由表 -> 知道要去 `Scout`
2. 找到对应的 `session`
3. 发送 RPC 请求: `await session.call_tool(...)`

---

## 🧪 验证结果

运行 `src/phase4/test_concierge_auto.py`：

**Case 1: 查门票**
> User: "广州小蛮腰门票"
> LLM: 决定调用 `search_poi`
> Concierge: 将请求转发给 `Scout Agent`
> Result: ✅ 成功返回 POI 列表

**Case 2: 查天气**
> User: "北京冷吗"
> LLM: 决定调用 `get_weather`
> Concierge: 将请求转发给 `Meteorologist Agent`
> Result: ✅ 成功返回天气实况

---

## 🎓 面试话术

### Q: 你的多 Agent 是怎么通信的？
> "我使用了 MCP (Model Context Protocol) 协议。
> 每个 Expert Agent (Scout, Meteorologist) 都是独立的 MCP Server 进程。
> 我的主 Orchestrator 作为一个 MCP Client，通过 Standard IO (stdio) 与子进程通信。
> 这种架构让系统具备极高的扩展性，新增一个 Agent 只需要启动一个新进程并连接即可，无需修改 Orchestrator 的核心代码。"

---

## ✅ 学习检查清单

- [x] 理解 MCP Client/Server 架构
- [x] 使用 `StdioServerParameters` 启动子进程
- [x] 实现动态工具发现 (`session.list_tools()`)
- [x] 完成多 Agent 协同调度

---

## 🚀 Phase 4 结项

恭喜！我们已经搭建起了一个**企业级**的 Agent 架构。
- **Scout**: 独立的 POI 搜素服务
- **Meteorologist**: 健壮的天气服务
- **Concierge**: 智能的调度中心

**Next: Phase 5 - 地理空间数据处理**
现在的搜索结果还是纯文本。
下一阶段，我们要引入**数据处理层**，学习如何处理经纬度、计算距离，甚至解决简单的路径规划问题。
