# Day 4.2: Meteorologist Agent (气象员) 🌤️

> **今日目标**: 打造一个"永远不会崩溃"的 Agent
> **核心成果**: `src/phase4/weather_agent.py`

---

## 📖 Part 1: 防御性编程 (Defensive Programming)

Scout Agent (Day 4.1) 假设一切顺利。
Meteorologist (Day 4.2) 假设**一切都会出错**。

### 🚨 常见风险
1. **用户乱输**: 用户输入 "New York" (API 没数据) 或者 "上海市" (API 只要 "上海")
2. **网络波动**: API 超时
3. **配置丢失**: 忘了配 `AMAP_API_KEY`

---

## 🔧 Part 2: 实战技巧

### 1. 输入清洗 (Input Cleaning)
用户经常会画蛇添足，比如输入 "上海市"。
高德 API 的 `adcode` 映射表通常只用简称。

```python
# 简单的清洗逻辑
clean_city = city.strip().replace("市", "")
city_code = CITY_CODES.get(clean_city)
```

### 2. 友好报错 (User-Friendly Errors)
**Bad**: `KeyError: 'New York'` (程序崩溃)
**Good**:
```python
if not city_code:
    return f"⚠️ 抱歉，我目前不支持 '{city}'。\n✅ 支持列表: 北京, 上海..."
```
这样 LLM 收到错误信息后，甚至可以据此回复用户："对不起，我暂时查不了纽约，但我可以查北京哦。"

### 3. 网络异常处理
显式捕获 `requests.Timeout` 和 `HTTPError`。
```python
try:
    resp.raise_for_status()
except requests.Timeout:
    return "❌ 请求超时，请稍后再试"
```

---

## 🧪 验证结果

运行 `src/phase4/test_weather_direct.py`：

**Case 1: 模糊输入**
> 输入: "上海市"
> 输出: ✅ 上海天气实况... (自动去掉了'市')

**Case 2: 越界输入**
> 输入: "纽约"
> 输出: ⚠️ 抱歉，我目前不支持...

---

## 🎓 面试话术

### Q: 你的 Agent 能够处理意外输入吗？
> "能。我在 Tool 的实现层引入了**防御性编程**。
> 比如在气象 Agent 中，我针对用户可能输入的'上海市'做了清洗，针对不支持的城市做了白名单校验。
> 重要的是，我返回的是**结构化的错误描述**而不是程序异常，这样上层的 Orchestrator LLM 可以理解这个错误，并优雅地转达给用户。"

---

## ✅ 学习检查清单

- [x] 实现参数清洗 (Data Cleaning)
- [x] 实现白名单校验 (Whitelist Validation)
- [x] 封装 Robust 的 FastMCP 服务

---

## 🚀 下一步

**Day 4.3: Concierge Agent (礼宾员) && 集成**
现在我们有两个独立的 Agent (Scout, Meteorologist)。
我们需要升级 `Orchestrator`，让它能够**动态连接**这两个微服务，而不是 import 静态函数。
我们将学习 MCP 的精华：**Client-Server 通信**。
