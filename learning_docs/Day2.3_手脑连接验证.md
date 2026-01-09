# Day 2.3: 手脑连接验证 🧠⚡🤚

> **今日目标**: 把"大脑"(LLM)和"手"(高德API)连接起来，实现自然语言驱动的真实互动
> **完成状态**: ✅ 已完成

---

## 📖 Part 1: 什么是"手脑连接"？

在 Day 2.1 和 2.2，我们分别测试了：
- **高德天气 API** (左手)
- **高德 POI API** (右手)

但它们都是独立运行的。
**"手脑连接"**是指：让已有的 **DeepSeek LLM (大脑)** 根据用户的自然语言指令，**自主决定**是用左手还是右手，并**自动执行**。

### 🔄 核心流程
1. **User**: "帮我查查北京天气"
2. **Brain (Prompt)**: 分析意图 -> `{ "tool": "get_weather", "args": {"city": "北京"} }`
3. **Hand (Code)**: 执行 `get_weather("北京")` -> 调用真实高德 API
4. **Result**: 返回真实数据

---

## 🔧 Part 2: 实战代码剖析

### 关键点 1: 代理冲突解决 ⚡
这是一个非常经典的工程问题：
- **DeepSeek API**: 需要翻墙 (Proxy: `127.0.0.1:7897`)
- **高德 API**: 国内服务，不走代理
- **冲突**: Python 脚本如果设置了全局代理，高德会报错；如果不设，DeepSeek 会报错。
- **解决**: 全局设置 `HTTP_PROXY` 给 DeepSeek 用，但在调用高德 `requests.get` 时显式传入 `proxies={"http": None}`。

### 关键点 2: 动态调度 (Orchestrator雏形)
```python
# 大脑思考
decision = json.loads(llm_response)

# 动态分发
if decision["tool"] == "get_weather":
    result = get_weather(decision["args"]["city"])
elif decision["tool"] == "search_poi":
    result = search_poi(...)
```

---

## 🧪 验证结果

我们成功实现了以下对话：

**Case 1: 天气查询**
> 用户: "帮我查查北京现在的天气"
> 大脑: 决定调用 `get_weather`
> 结果: ✅ 北京天气: 多云, 温度: 6℃... (真实数据)

**Case 2: 找吃的**
> 用户: "上海有哪些好吃的必胜客？"
> 大脑: 决定调用 `search_poi`
> 结果: ✅ 必胜客(新世界城店)... (真实地址)

---

## 🎓 面试话术

### Q: 你的 Agent 是如何处理网络环境复杂的 API 调用的？
> "在开发过程中，我遇到了混合网络环境的挑战。DeepSeek 模型需要走代理访问，而高德、百度等国内服务需要直连。
> 我在底层 HTTP 客户端层面做了精细化控制：在应用启动时加载全局代理以确保 LLM 可用，
> 但在封装国内 Service Tool 时，显式配置 `proxies=None` 绕过代理。
> 这体现了对 `requests` 库和网络层的深入理解。"

---

## 📁 代码文件

| 文件 | 用途 |
|------|------|
| `src/phase2/brain_hand_connect.py` | 手脑连接验证完整脚本 |

---

## ✅ 学习检查清单

- [x] 理解如何用 Prompt 描述工具给 LLM
- [x] 解决 Proxy 冲突 (DeepSeek vs Amap)
- [x] 实现 JSON 格式的意图识别
- [x] 成功串联 LLM 和 真实 API

---

## 🚀 Phase 2 结项

我们已经完成了基础设施搭建：
1. **API 配置**: DeepSeek & 高德 (Web服务) 准备就绪
2. **连接验证**: 手脑已通，可以交互
3. **工程坑**: 解决了代理冲突、Key类型匹配等实际问题

**Next: Phase 3 - 构建真正的 HelloAgent** (开始写正式的 Worker 类)
