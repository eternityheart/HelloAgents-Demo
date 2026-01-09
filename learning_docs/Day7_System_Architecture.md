# 基于 HelloAgents 的多智能体旅行规划系统设计与实现

## 1. 系统概述
本项目基于 **HelloAgents** 框架，构建了一个多智能体（Multi-Agent）协同的智能旅行规划系统。系统采用了 **Orchestrator-Workers**（大脑-手脚）架构模式，通过引入规划协调 Agent（Orchestrator）负责用户意图解析、任务拆解与 Agent 调度，将复杂的行程规划任务拆分为景点搜索、天气查询、酒店推荐等子任务，交给功能型 Agent（Workers）执行。

## 2. 核心架构设计

系统自顶向下分为四层：
1.  **用户交互层 (Frontend)**: 基于 Vue3/Vanilla JS + 高德地图 API，实现可视化交互。
2.  **服务层 (Backend Service)**: 基于 FastAPI，提供 HTTP SSE 流式接口，解耦前后端。
3.  **编排层 (Orchestrator)**: `HelloAgents` 核心大脑，负责任务规划与分发。
4.  **能力层 (Workers & MCP Tools)**: 专家 Agent 与标准化工具集。

---

## 3. 详细功能实现说明

### 3.1 🧠 编排层：意图解析与任务拆解 (Orchestrator)
**对应文件**: `src/phase3/orchestrator.py`

Orchestrator 是系统的"指挥官"。它不直接执行具体任务，而是通过分析用户输入，生成结构化的行动计划。

*   **意图解析 (Intent Parsing)**: 使用 LLM 配合 `Pydantic` 强类型校验，从自然语言中提取关键要素（目的地、天数、偏好）。
*   **任务拆解 (Task Decomposition)**: 将"做一份攻略"拆解为具体的 Action Sequence，例如：
    1.  调用 `Meteorologist` 查询目标城市天气。
    2.  调用 `Scout` 搜索符合偏好的景点 (POI)。
    3.  调用 `Concierge` 整合信息并生成行程。
*   **代码实现**:
    ```python
    class TravelPlan(BaseModel):
        destination: str
        days: int
        needed_actions: List[str]  # e.g. ["check_weather", "search_poi"]
    
    # 通过 response_format={"type": "json_object"} 强制 LLM 输出符合 Schema 的 JSON
    ```

### 3.2 🛠️ 能力层：多 Agent 协同与 MCP 工具封装
**对应文件**: `src/phase4/agents/`

我们将行程规划拆分为三个独立的职责方向，每个 Agent 专注自己的领域：

1.  **👀 侦察兵 (Scout Agent)**
    *   **职责**: 负责寻找景点、餐厅等 POI (Point of Interest)。
    *   **能力**: 封装高德地图 `PlaceSearch` API。
    *   **MCP 实现**: 通过 MCP 协议将高德 API 封装为标准工具 `search_poi(keyword, city)`。

2.  **⛅ 气象员 (Meteorologist Agent)**
    *   **职责**: 提供精准的天气预报，辅助行程决策（如雨天推荐室内）。
    *   **能力**: 封装高德地图 `Weather` API。
    *   **MCP 实现**: 工具 `get_weather(city)`，返回包含温度、天气现象的结构化数据。

3.  **🛎️ 礼宾员 (Concierge Agent/Fusion)**
    *   **职责**: 信息融合。它接收前两个 Agent 的输出，结合用户偏好，生成最终的自然语言行程建议，并计算推荐理由。

### 3.3 🔌 MCP 思想与外部服务集成
**对应文件**: `src/phase2/fastmcp_tools.py`

系统采用 **Model Context Protocol (MCP)** 思想（使用 FastMCP 库简化实现）来管理工具：
*   **解耦**: Agent 不需知道高德 API 的具体 URL 或参数结构，只需调用标准化的 Python 函数。
*   **自治**: Agent 根据上下文自主决定何时调用哪个工具（Function Calling）。

### 3.4 🚀 服务层：HTTP 接口与流式传输
**对应文件**: `src/phase6/main.py`

为了支持类似 ChatGPT 的打字机体验，后端采用 FastAPI 构建：
*   **解耦 Agent 逻辑**: 将长时间运行的 Agent 推理过程封装在异步任务中。
*   **SSE (Server-Sent Events)**: 使用 `/chat/stream` 接口，将 Agent 的思考过程（Thinking）、工具调用（Tool Call）和最终回复（Final Answer）实时推送给前端。

### 3.5 🎨 前端：可视化与 Agentic Workflow 落地
**对应文件**: `src/phase7/` (`doraemon.css`, `app.js`, `map.html`)

前端不仅是一个聊天窗口，更是 Agent 思维过程的可视化容器：

1.  **实时反馈**: 解析 SSE流，区分显示 "正在思考..."、"正在调用天气工具..." 等状态，让用户感知 System 1 (快) 和 System 2 (慢) 的工作流。
2.  **地图可视化**:
    *   接收后端返回的 POI 坐标数据。
    *   使用高德地图 JS API 在画布上绘制 Marker。
    *   **路径规划**: 调用 `AMap.Walking` 和 `AMap.Driving` 接口，将抽象的行程转化为地图上的实体路线。
3.  **UI 设计**: 采用哆啦A梦主题（Doraemon HUD），通过 CSS 变量管理 `doraemon-blue` 等主题色，配合 Glassmorphism 动效，提供沉浸式体验。

---

## 4. 总结
本系统完整展示了从 **"基于规则"** 到 **"基于 Agent"** 的范式转变。通过 HelloAgents 框架，我们成功将一个模糊的 User Prompt 转化为了精确的 API 调用和可视化的地图方案，验证了多智能体系统在解决复杂现实问题上的巨大潜力。
