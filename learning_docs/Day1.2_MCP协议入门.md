# Day 1.2: MCP协议 - 让Agent学会使用工具 🔧

> **今日目标**: 理解 MCP 协议如何让 LLM "长出手脚"，能够调用外部工具
> **完成状态**: ✅ 已完成

---

## 📖 Part 1: 概念理解

### 🎭 比喻：万能插座的故事

想象你买了很多电器：日本的电饭煲、英国的烧水壶、中国的电风扇...

**没有标准之前**：每个电器都需要单独买转换头 → M×N 个适配器 😵

**有了标准之后** (USB-C)：所有设备统一接口 → M+N 个适配器 🎉

```
              MCP 就是 AI 世界的 "USB-C"
              
  没有MCP:  维护成本 = M个模型 × N个API = M×N 套代码 💀
  有了MCP:  维护成本 = M + N 套代码 ✨
```

### 🏗️ MCP 架构图

```
┌──────────────────┐
│   你的 Agent     │  ← MCP Client (使用工具的人)
│   (DeepSeek)     │
└────────┬─────────┘
         │ MCP协议 (JSON-RPC)
┌────────▼─────────┐
│   MCP Server     │  ← 工具提供者
│   (FastMCP)      │
├──────────────────┤
│  @tool 天气查询   │
│  @tool 景点搜索   │
└──────────────────┘
```

---

## 🔧 Part 2: 动手实验

### 实验 A: MCP 工具定义 (`src/day1/day1_2_mcp_tool.py`)

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator")

@mcp.tool()
def add(a: int, b: int) -> int:
    """把两个数字加起来"""  # ← LLM 会读取这个描述！
    return a + b
```

**关键点**: 
- `@mcp.tool()` 把普通函数变成"可被LLM发现的工具"
- **docstring 非常重要** - LLM 根据它来决定是否使用该工具

### 实验 B: Function Calling (`src/day1/day1_2_function_calling.py`)

**三阶段流程**:
```
1. 用户提问 → LLM 分析意图 → 决定是否调用工具
2. 执行工具 → 获取真实数据
3. 反馈结果 → LLM 生成自然语言回答
```

---

## 🧪 测试验证结果

### 测试 A: MCP 工具单独测试
```
测试 1: add(3, 5)     → 8      ✅ 通过
测试 2: multiply(4, 7) → 28     ✅ 通过
测试 3: get_weather('北京') → "晴天，气温 -2°C ~ 8°C" ✅
```

### 测试 B: Function Calling 完整流程
| 用户问题 | LLM 决策 | 结果 |
|----------|----------|------|
| "15 加 27 等于多少？" | 调用 `add` | 42 ✅ |
| "北京今天天气怎么样？" | 调用 `get_weather` | 晴天 ✅ |
| "你好，介绍一下你自己" | **不需要工具** | 直接回答 ✅ |

---

## 🎓 面试话术

### Q: 什么是 MCP？
> "MCP (Model Context Protocol) 是一个标准化协议，用于 LLM 与外部工具的通信。它解决了'集成税'问题——通过统一接口，一个工具可以被多个模型复用，降低了 M×N 的集成成本到 M+N。"

### Q: docstring 在 Function Calling 中有什么作用？
> "docstring 不仅是给开发者看的文档，更是 LLM 理解工具用途的关键。MCP 会把 docstring 作为工具描述发送给 LLM，LLM 根据这个描述来决定是否调用该工具。清晰的 docstring 直接影响工具选择的准确率。"

### Q: Function Calling 的执行流程是什么？
> "分三个阶段：第一阶段，LLM 分析用户意图，决定是否需要工具以及调用哪个工具；第二阶段，执行工具获取真实数据；第三阶段，把工具结果反馈给 LLM，生成最终的自然语言回答。这是 ReAct (Reasoning + Acting) 模式的基础。"

---

## 📁 代码文件

| 文件 | 用途 |
|------|------|
| `src/day1/day1_test.py` | API 连接测试 |
| `src/day1/day1_2_mcp_tool.py` | MCP 工具定义示例 |
| `src/day1/day1_2_function_calling.py` | Function Calling 完整演示 |

---

## ✅ 学习检查清单

- [x] 理解 MCP 解决的问题（USB-C 比喻）
- [x] 理解 MCP Client-Server 架构
- [x] 掌握 `@mcp.tool()` 装饰器用法
- [x] 理解 docstring 对 LLM 的重要性
- [x] 理解 Function Calling 三阶段流程
- [x] 能用自己的话解释给面试官

---

## 🚀 下一步

**Day 1.3: 框架对比与选型**
- 对比 HelloAgents、LangGraph、CrewAI
- 理解各自的适用场景
- 绘制框架对比脑图
