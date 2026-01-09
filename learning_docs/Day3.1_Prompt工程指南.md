# Day 3.1: Prompt Engineering 进阶 💬

> **今日目标**: 告别"自然语言对话"，掌握"协议级" Prompt 编写技巧
> **核心成果**: `system_prompts.py` (模块化 Prompt 管理)

---

## 📖 Part 1: 为什么你需要"专业版" Prompt？

### ❌ 新手写法 vs ✅ 专家写法

**新手写法**:
> "你是一个旅行助手，帮我查查天气和景点，要是不知道就说不知道。"

🚨 **问题**:
- 输出不可控（一会儿 markdown，一会儿纯文本）
- 无法与代码对接（Python 很难提取 "北京晴天" 里的数据）
- 容易产生幻觉

**专家写法 (RAP 框架)**:
- **R**ole (角色): "你是智能调度中枢..."
- **A**bility (能力): "你有 get_weather, search_poi..."
- **P**rotocol (协议): "必须输出如下 JSON 格式..."

---

## 🔧 Part 2: 模块化 Prompt 设计

我们创建了 `src/phase3/system_prompts.py`，把 Prompt 拆成了三部分：

### 1. Core Identity (你是谁)
```python
CORE_IDENTITY = """
你是一个名为 "HelloAgent" 的智能旅行规划助手。
...
"""
```

### 2. Tool Definitions (你会什么)
这是连接 LLM 和 Python 代码的桥梁。必须清晰定义参数！
```python
TOOL_DEFINITIONS = """
1. get_weather(city: str) -> str
   - 参数：city (必须是城市名)
2. search_poi(city: str, keyword: str, poi_type: str)
   - 此处定义枚举值: "景点", "餐厅", "酒店"
"""
```

### 3. Output Protocol (你要怎么说)
这是最关键的一步。强制 LLM 使用 JSON Mode。
```python
OUTPUT_PROTOCOL = """
分析用户意图，输出 JSON：
{
    "type": "tool_call",
    "tool_name": "get_weather",
    "args": { "city": "..." },
    "thought": "你的思考过程"
}
"""
```

---

## 🧪 测试结果

运行 `src/phase3/test_prompt.py`：

**Case 1: 复杂指令**
> 用户: "我想去上海玩，帮我搜一下附近的迪士尼酒店"

**LLM 输出 (JSON)**:
```json
{
  "type": "tool_call",
  "tool_name": "search_poi",
  "args": {
    "city": "上海",
    "keyword": "迪士尼",
    "poi_type": "酒店"
  },
  "thought": "用户想去上海玩，并搜索附近的迪士尼酒店..."
}
```

✅ **完美提取了三个参数！**

---

## 🎓 面试话术

### Q: 你的 Prompt 是怎么管理的？
> "我没有把 Prompt 散落在代码里，而是采用了模块化管理 (`system_prompts.py`)。
> 我使用了 **RAP 框架 (Role-Ability-Protocol)** 来构建 System Prompt。
> 特别是在 Protocol 层，我强制 LLM 输出 **JSON 格式**，配合 `response_format={"type": "json_object"}`，
> 解决了大模型输出不稳定的工程难题。"

### Q: 如何让 LLM 准确调用工具？
> "关键在于 **Tool Definition** 的清晰度。我不只写函数名，还详细定义了参数类型和枚举值（如 poi_type 只能是 景点/餐厅）。
> 这样 LLM 不仅是'理解'意图，还能像编译器一样进行'参数填充'。"

---

## ✅ 学习检查清单

- [x] 理解 RAP Prompt 框架
- [x] 为什么必须要求 JSON 输出？(为了代码好解析)
- [x] 掌握 Tool Analysis 的 Prompt 写法
- [x] 成功提取复杂参数 (上海/迪士尼/酒店)

---

## 🚀 下一步

**Day 3.2: 结构化输出封装**
现在我们拿到了 JSON 字符串，下一步要用 Python 的 `Pydantic` 把它变成强类型的对象，防止 LLM 有时候少写一个括号导致程序崩溃。
