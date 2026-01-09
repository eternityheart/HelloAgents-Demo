# Day 3.2: 结构化输出 (Structured Output) 🧱

> **今日目标**: 给 LLM 戴上"紧箍咒"，确保它吐出的永远是可执行的代码对象
> **核心成果**: `src/phase3/models.py` (Pydantic 模型定义)

---

## 📖 Part 1: 为什么要用 Pydantic？

在 Day 3.1 中，我们让 LLM 输出了 JSON 字符串。
但在工程实现中，**字符串是不可信的**。

### 🚨 常见灾难现场
1. **类型错误**: `{"age": "18"}` (字符串) vs `{"age": 18}` (数字)
2. **字段缺失**: 忘了写 `thought` 字段
3. **幻觉参数**: 调用 `get_weather` 却传了 `date="tomorrow"` (函数根本没这个参数)

**Pydantic** 的作用就是把不可信的 `dict/json` 强转为可信的 `class` 对象。

---

## 🔧 Part 2: 实战代码

### 1. 定义"模具" (Models)
我们在 `src/phase3/models.py` 定义了两种核心结构：

```python
class AgentAction(BaseModel):
    """当 LLM 想要执行动作时"""
    type: Literal["tool_call"]
    tool_name: str
    args: Dict[str, Any]  # 自由字典，但必须是字典
    thought: str

class AgentResponse(BaseModel):
    """当 LLM 想要回复用户时"""
    type: Literal["response"]
    content: str
    thought: str
```

### 2. 强类型解析
在 `src/phase3/test_structured_output.py` 中：

```python
# 1. 获取 LLM 的 JSON 字符串
content = response.choices[0].message.content

# 2. 转换为 Python 字典
data = json.loads(content)

# 3. Pydantic 校验 (最关键的一步!)
if data["type"] == "tool_call":
    # 如果这里报错，说明 LLM 没遵守协议
    action = AgentAction(**data) 
    print(action.tool_name)  # IDE 可以自动补全!
```

---

## 🧪 实验现象

**Case 1: 查询门票 (未定义工具)**
> 用户: "广州小蛮腰门票多少钱？"
> LLM 输出: `{"type": "response", "content": "抱歉，我无法查询门票..."}`
> **解析结果**: 成功映射为 `AgentResponse` 对象 ✅
> **点评**: LLM 非常诚实！因为它发现 `get_weather` 和 `search_poi` 都没法查门票，所以选择了 `response` 模式。

**Case 2: 闲聊**
> 用户: "这就去"
> LLM 输出: `{"type": "response", "content": "好的...", "thought": "..."}`
> **解析结果**: 成功映射为 `AgentResponse` 对象 ✅

---

## 🎓 面试话术

### Q: 如果 LLM 输出的 JSON 格式不对怎么办？
> "我使用了 **Pydantic** 进行防御性编程。
> 如果 `AgentAction(**data)` 抛出 ValidationError，我会捕获这个异常。
> 在生产环境中，我会把这个错误信息（比如 'missing field: tool_name'）作为 System Prompt 的一部分**返还给 LLM**，让它进行 **Self-Correction (自我修正)**，重新生成正确的 JSON。这在 Agent 开发中称为 'Reflexion' 机制。"

### Q: 为什么不直接用 dict？
> "使用 Pydantic 对象的好处是 **Type Hinting (类型提示)**。
> 在后续的代码（Orchestrator）中，我可以直接使用 `action.args['city']`，IDE 会知道它是什么类型。
> 这在大型项目中能显著减少 'AttributeError' 甚至逻辑错误，让代码更健壮。"

---

## ✅ 学习检查清单

- [x] 理解 JSON String vs Python Object 的区别
- [x] 掌握 Pydantic `BaseModel` 的定义
- [x] 理解 `Literal` 类型在区分消息类型中的作用
- [x] 成功解析 LLM 输出为 Python 对象

---

## 🚀 下一步

**Day 3.3: 状态管理 (Context Memory)**
现在的 Agent 还是"金鱼记忆"（只有7秒）。
如果我们说："帮我查北京天气"，它查了。
然后紧接着问："那上海呢？" —— 它可能会问："上海什么？"
因为它忘了上一句我们聊的是天气。
下一节，我们要给它加上 **Memory**。
