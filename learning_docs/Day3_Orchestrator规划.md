# Phase 3: 构建 Agent 大脑 (Orchestrator) 🧠

> **本阶段目标**: 将零散的 API 调用（Day 2 成果）封装成真正的企业级 AI Agent 架构。
> **关键词**: `Prompt Engineering`, `Structured Output`, `State Management`

---

## 📅 Day 3 学习路线图

### Day 3.1: Prompt Engineering 进阶
- **目标**: 写出"生产级"的 System Prompt
- **核心概念**:
    - Role Context (角色设定)
    - Capability Constraints (能力边界)
    - Output Format (输出规范 - JSON)
    - Few-Shot Prompting (少样本提示)

### Day 3.2: 结构化输出 (Structured Output)
- **目标**: 让 LLM 稳定输出 JSON，而不是"废话"
- **核心概念**:
    - Pydantic 模型定义
    - JSON Mode (DeepSeek 支持)
    - 容错解析 (Retry 机制)

### Day 3.3: 状态管理与上下文
- **目标**: 让 Agent 记住"刚才聊了什么"
- **核心概念**:
    - `messages` 列表维护
    - Token 管理 (避免上下文溢出)

---

## 🏗️ 架构演进

**Before (Day 2.3)**:
```python
# 简单的脚本
def brain_process(query):
    # 直接调 API
    ...
```

**After (Phase 3)**:
```python
# 面向对象的各类
class Orchestrator:
    def __init__(self):
        self.memory = []
        self.system_prompt = "..."

    def think(self, user_input) -> Plan:
        # 1. 历史上下文组装
        # 2. 调用 LLM
        # 3. 解析 JSON
        # 4. 返回行动计划
```

---

## 📝 交付物清单

1. `learning_docs/Day3.1_Prompt工程指南.md`
2. `src/phase3/system_prompts.py` (Prompt 管理)
3. `src/phase3/orchestrator.py` (核心类)

---

## 🚀 开始第一步: Day 3.1 Prompt Engineering

我们将学习如何写出 DeepSeek 能完美理解的 Prompt。
不再是简单的 "你是旅行助手"，而是包含详细工具定义和输出约束的 "协议"。
