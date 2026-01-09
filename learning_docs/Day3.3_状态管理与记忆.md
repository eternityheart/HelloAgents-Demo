# Day 3.3: 状态管理与记忆 (State Management) 🧠

> **今日目标**: 赋予 Agent "长期记忆"，让它能进行多轮对话
> **核心成果**: `src/phase3/orchestrator.py` (SimpleOrchestrator)

---

## 📖 Part 1: 上下文 (Context) 的本质

在 LLM 的世界里，没有真正的"记忆"。
每一次 API 调用都是**独立**的。
为了假装有记忆，我们需要把**之前所有的对话记录**打包，每次都重新发给 LLM。

### 📝 Messages 列表结构

```python
self.messages = [
    {"role": "system", "content": "..."},  # 身份设定
    {"role": "user", "content": "查北京天气"}, # 第1轮
    {"role": "assistant", "content": "Tool Call..."},
    {"role": "user", "content": "Tool Output..."},
    {"role": "user", "content": "那上海呢？"}  # 第2轮 (LLM 能看到上面的"天气"语境)
]
```

---

## 🔧 Part 2: 实战代码

我们在 `src/phase3/orchestrator.py` 中实现了 `SimpleOrchestrator` 类：

### 1. 初始化记忆
```python
def __init__(self):
    self.messages = [
        {"role": "system", "content": get_orchestrator_prompt()}
    ]
```

### 2. 对话循环 (Chat Loop)
1. **Append**: 把用户的话加入 `messages`
2. **Think**: 调用 LLM (带上所有 `messages`)
3. **Act**: 如果是 Tool Call，执行代码
4. **Update**: 把工具结果加入 `messages` (重要!)
5. **Re-Think**: 再次调用 LLM，让它根据工具结果生成回复

---

## 🧪 实验结果 (见证奇迹的时刻)

**User**: "帮我查查北京的天气"
**Agent**: (调用 API) ...北京 6度...

**User**: "那上海呢？"
**Agent**:
> 🧠 Thinking...
> 🤔 Thought: **用户想查询上海的天气** (它懂了!)，我需要调用 get_weather...
> ✅ Tool Output: 上海 7度...

**点评**:
这就是 **Context-Aware** (上下文感知)。
LLM 通过查看历史记录，知道"那上海呢"指的就是"上海的天气"，而不是上海的房价或人口。

---

## ⚠️ 工程挑战: JSON 脆弱性

在实验中，你可能会发现偶尔会报错：
`JSONDecodeError: Expecting value...`

这是因为 DeepSeek V3 (Beta) 在长上下文中有时会：
1. 输出不完整的 JSON
2. 混入 Markdown 格式 (` ```json ... `)
3. 突然输出纯文本

**解决方案 (Phase 4 预告)**:
- **Retry 机制**: 解析失败就让 LLM 重试
- **Robust Parser**: 使用更强的解析库 (如 `dirty-json`)
- **Schema Validation**: 使用 `Instructor` 或 `Guidance` 等库

---

## 🎓 面试话术

### Q: 你的 Agent 是如何维护状态的？
> "我设计了一个 `SimpleOrchestrator` 类，内部维护一个 `messages` 列表作为 Short-term Memory。
> 每次对话都会追加 User Input、Assistant Thought 和 Tool Output。
> 特别要注意的是，**Tool Output 也必须作为历史记录的一部分**，这样 LLM 才能知道它刚才查到了什么，从而生成最终回复。"

### Q: 如果对话太长怎么办？
> "随着对话轮数增加，Token 消耗会线性增长甚至超出窗口限制。
> 在这个 Demo 中我没有处理，但在生产环境我会引入 **Memory Management** 策略，
> 比如 'Sliding Window' (只保留最近N轮) 或 'Summary Memory' (让 LLM 定期总结之前的对话存入 System Prompt)。"

---

## ✅ 学习检查清单

- [x] 理解 Messages 列表的作用
- [x] 为什么工具结果也要存入 History？
- [x] 成功验证多轮对话 ("那上海呢？")
- [x] 遇到并理解 JSON 解析的不稳定性问题

---

## 🚀 Phase 3 结项

我们已经手写了一个最小功能的 Agent 框架！
它有手 (Tools)、有脑 (LLM)、有记忆 (Memory)。

**Next: Phase 4 - 专家 Agent 开发**
我们将构建更专用的 Agent (Scout, Meteorologist)，并把工具封装得更标准 (FastMCP)。
