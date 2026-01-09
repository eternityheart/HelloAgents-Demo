# Day 6.1: FastAPI 基础与 SSE 流式传输 🌊

> **今日目标**: 告别"死等"的 HTTP 请求，拥抱"涓涓细流"的实时响应。
> **核心成果**: `src/phase6/main.py`

---

## 📖 Part 1: WebSocket vs SSE (面试必考)

你刚才的困惑非常普遍。很多初学者以为"实时"就等于 "WebSocket"。
其实对于 AI Agent 场景，**SSE (Server-Sent Events)** 往往是更优选。

### 对比表

| 特性 | WebSocket 📞 | SSE (Server-Sent Events) 📻 |
|:---|:---|:---|
| **通信方向** | 双向 (Two-way) | 单向 (Server -> Client) |
| **协议** | TCP (需要升级协议) | 标准 HTTP (只是 Content-Type 不同) |
| **适用场景** | 即时通讯 (IM)、游戏、股票交易 | **AI 生成回复**、新闻推送、日志监控 |
| **实现难度** | 较复杂 (握手、心跳) | **极其简单** (就像下载一个无限长的文件) |
| **断线重连** | 需要自己写逻辑 | 浏览器内置自动重连 |

### 结论
ChatGPT 的网页版主要使用 **SSE**。
因为用户发一句，AI 回几十句，这典型的**一问多答**场景，非常适合 SSE。

---

## 🔧 Part 2: 实战代码解析

### 1. 服务端 (`main.py`)
FastAPI 对 SSE 的支持非常优雅。核心就是 `StreamingResponse`。

```python
async def fake_streamer():
    text = "Hello..."
    for char in text:
        # SSE 标准格式: 必须以 "data: " 开头，以 "\n\n" 结尾
        yield f"data: {char}\n\n"
        await asyncio.sleep(0.1)

@app.get("/stream")
async def stream():
    return StreamingResponse(fake_streamer(), media_type="text/event-stream")
```

### 2. 客户端 (`test_stream.py`)
如果你用 Python 的 `requests` 库测试：
```python
# 关键在于 stream=True
response = requests.get(url, stream=True)
for line in response.iter_lines():
    # 处理每一行数据
    ...
```

---

## 🧪 验证结果

1. 我们启动了服务器 (`python main.py`)
2. 运行了测试脚本 (`python test_stream.py`)
3. 终端里不仅仅是打印了一句话，而是**一个字一个字蹦出来的**！
   > H...e...l...l...o...

这就是前端用户看到的"ChatGPT 打字机效果"。

---

## 🎓 面试话术

### Q: 你的 Agent 后端为什么用 SSE 而不用 WebSocket？
> "因为 Agent 的对话场景主要是'用户发一条指令，AI 流式返回长文本'。
> SSE 基于标准 HTTP，对防火墙友好，断线自带重连，且不需要处理 WebSocket 复杂的握手和心跳机制。
> 对于这种单向高频数据流，SSE 是更轻量级且符合 RESTful 风格的解决方案。"

---

## ✅ 学习检查清单

- [x] 理解 WebSocket 与 SSE 的区别 (单向 vs 双向)
- [x] 使用 FastAPI 实现 `StreamingResponse`
- [x] 理解 SSE 的数据格式 (`data: ... \n\n`)

---

## 🚀 下一步

**Day 6.2: 集成 Orchestrator (真正的大脑)**
现在的 `/stream` 只是个假数据生成器。
下一步，我们要把 Phase 3 做的 `SimpleOrchestrator` 塞进去。
这就涉及到一个大问题：
Orchestrator 是**同步 (Sync)** 代码，FastAPI 是**异步 (Async)** 的。
如果在 Async 函数里直接跑 Sync 代码，会把服务器**卡死**。

我们要学习 Python 的 `async/await` 改造！
