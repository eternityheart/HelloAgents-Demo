# Day 6.2: 异步编排 (Async Orchestrator) 🧠

> **今日目标**: 给 AI 能够"一心二用"的能力，避免一个用户的思考卡死整个即时通讯。
> **核心成果**: `src/phase6/async_agent.py`

---

## 📖 Part 1: 为什么需要 Async？

### 场景模拟
假设我们的 API 是同步的 (`def chat`)，处理一个请求需要 10 秒（LLM 思考 + 查天气）。
由于 Python 的 GIL (全局解释器锁) 和 uvicorn 的单线程特性：
- **用户 A** 发起请求 -> 服务器开始计算 (第 1 秒)
- **用户 B** 发起请求 -> 服务器：*“由于 A 还没结束，请您排队卡死在这里”* (等待 9 秒)
- **用户 A** 结束 -> **用户 B** 才开始处理。

这在 Web 服务中是 **灾难**。

### 解决方案: Async/Await
我们使用 `async def`，当代码遇到 `await` (比如等待 API 返回) 时，会把 CPU 让出来去处理其他用户的请求。

---

## 🔧 Part 2: 实战技巧 (Sync与Async的混搭)

我们在 Phase 3 写的 `tools.py` 是同步代码 (使用了 `requests`)。
如果在 `async def` 中直接调用 `requests.get`，依然会**阻塞**整个事件循环！

### 核心黑魔法: `asyncio.to_thread`
我们可以把同步代码"扔"到另一个线程里去跑，主线程继续接客。

```python
# ❌ 错误做法：直接调用，卡死全场
# result = get_weather("Beijing")

# ✅ 正确做法：扔到线程池
import asyncio
loop = asyncio.get_running_loop()
result = await loop.run_in_executor(None, get_weather, "Beijing")
```
*(在 Python 3.9+ 中可以直接用 `asyncio.to_thread(get_weather, "Beijing")`，代码更简洁，但我展示的是兼容性更强的写法)*

---

## 🏗️ 架构模式: 流式生成器

我们的 `AsyncOrchestrator` 不再返回一个巨大的 JSON，而是返回一个 **Generator** (生成器)。
它像一个"前线记者"，不断汇报进展：

1. `yield "data: 🧠 思考中..."`
2. `yield "data: 🛠️ 调用工具..."`
3. `yield "data: ✅ 拿到结果..."`
4. `yield "data: 🤖 最终回复..."`

前端只需要监听这个频道，就能实时展示 AI 的心路历程。

---

## 🧪 验证结果

运行 `src/phase6/test_integration.py`：
- 你能看到 "🧠 正在思考..." 立即出现。
- 随后 "🛠️ 需要使用工具: get_weather" 出现。
- 最后 "北京天气..." 一个字一个字蹦出来。
- 整个过程非常丝滑，没有漫长的白屏等待。

---

## 🎓 面试话术

### Q: 如果你的 Tool 是 CPU 密集型的(比如图片处理)，在 FastAPI 里怎么跑？
> "FastAPI 默认的 `def` 路由会在线程池运行，但 `async def` 路由在主线程运行。
> 如果我有 CPU 密集型任务，或者必须使用同步 IO 库 (如 requests/pandas)，我会使用 `asyncio.to_thread` 将其调度到单独的线程池中执行，避免阻塞主 Event Loop，保证高并发下的响应能力。"

---

## ✅ 学习检查清单

- [x] 理解 Async/Await 对高并发的意义
- [x] 掌握在 Async 环境下调用 Sync 代码的方法 (`run_in_executor`)
- [x] 实现复杂的流式业务逻辑 (Think -> Tool -> Response)

---

## 🚀 Phase 6 结项

现在，我们拥有了一个**真正的 Backend**：
- **接口**: RESTful API + SSE
- **逻辑**: 异步 Orchestrator
- **能力**: 查天气、搜周边

有了这个后端，前端（无论是 Web 还是 App）只需要对接 `POST /chat/stream`，就能获得和 ChatGPT 一样的体验。

**Next: Phase 7 - 前端可视化 (Web UI)**
是时候给我们的 AI 穿上漂亮的衣服了！我们将在 Day 6.3 简单体验一下 Swagger UI，然后进入 Phase 7 写一个真正的聊天界面。
