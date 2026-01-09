# Phase 6: 后端服务化 (Backend Service) ⚡

> **本阶段目标**: 将终端里运行的 Python 脚本，包装成标准的可供前端或 App 调用的 HTTP API。
> **关键词**: `FastAPI`, `SSE (Server-Sent Events)`, `Async/Await`

---

## 📅 Day 6 学习路线图

### Day 6.1: FastAPI 基础与 SSE 流式响应 🌊
- **目标**: 搭建 API 骨架，实现打字机效果的流式输出
- **核心概念**:
    - FastAPI 路由定义 (`@app.post`)
    - Pydantic 模型作为 API 契约
    - `EventSourceResponse` (SSE) 原理

### Day 6.2: 集成 Orchestrator 🧠
- **目标**: 将 Phase 3 的 `SimpleOrchestrator` 接入 API
- **核心概念**:
    - 依赖注入 (Dependency Injection)
    - 异步化改造 (Sync to Async)
    - 真实 Agent 的流式日志回显

### Day 6.3: API 调试与文档 📚
- **目标**: 使用 Swagger UI 调试接口
- **核心概念**:
    - OpenAPI 自动生成文档
    - `curl` 测试流式接口

---

## 🏗️ 架构演进

**Before (Phase 5)**:
用户只能在 VS Code 的终端里输入 `python run_agent.py` 来和 Agent 聊天。

**After (Phase 6)**:
用户可以通过浏览器访问 `http://localhost:8000/docs`，或者未来通过 React 前端与之交互。
Agent 的思考过程（Thinking...）和工具调用结果，会通过 **SSE** 实时推送到前端，而不是等几十秒一次性返回。

---

## 📝 交付物清单

1. `src/phase6/main.py` (FastAPI 入口)
2. `src/phase6/api_models.py` (请求/响应模型)
3. `src/phase6/test_api.py` (API 测试脚本)

---

## 🚀 开始第一步: Day 6.1 FastAPI 基础

为什么选 **FastAPI**？
因为它快、原生支持异步 (Async)、自动生成文档。
更重要的是，它对 **SSE (流式传输)** 的支持非常友好，这对于 AI Agent 这种"边想边说"的应用场景至关重要。
