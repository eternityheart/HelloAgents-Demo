# HelloAgents 多智能体旅行规划系统 🌍✈️

> **边学边做**: 14天掌握AI Agent全栈开发，从小白到面试无忧！

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green)
![Vue3](https://img.shields.io/badge/Vue-3.x-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 项目简介

这是一个**教育性质**的多智能体旅行规划系统，基于 [Datawhale HelloAgents](https://github.com/datawhalechina/hello-agents) 框架重构。

**核心特点**:
- 🧠 **Orchestrator-Workers模式**: 大脑+手脚的智能协作
- 🔌 **MCP协议**: 标准化工具调用，降低集成成本
- 🌊 **SSE流式传输**: 实时展示Agent思考过程
- 🗺️ **地图可视化**: 高德地图API集成

## 📁 项目结构

```
agentdemo1/
├── src/                        # 源代码
│   ├── phase0_hello_agent.py   # Phase 0: Hello World Agent
│   ├── phase1_function_calling.py  # Phase 1: 工具调用
│   ├── phase2_orchestrator.py  # Phase 2: 意图提取
│   ├── phase3_specialists.py   # Phase 3: 专家Agents
│   └── config.py               # 配置管理
├── requirements.txt            # Python依赖
├── .env.example               # 环境变量模板
└── README.md                  # 本文件
```

## 🚀 快速开始

### 1. 环境准备
```bash
# 进入项目目录
cd e:\antiPro\agentdemo1

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置API密钥
```bash
# 复制配置模板
copy .env.example .env

# 编辑.env，填入你的密钥
# DEEPSEEK_API_KEY=sk-xxxxx
# AMAP_API_KEY=xxxxx
```

### 3. 运行示例

```bash
# Phase 0: Hello Agent
python src/phase0_hello_agent.py

# Phase 1: Function Calling
python src/phase1_function_calling.py

# Phase 2: Orchestrator
python src/phase2_orchestrator.py

# Phase 3: 专家Agents
python src/phase3_specialists.py
```

## 📚 学习路线

| 阶段 | 内容 | 时间 |
|------|------|------|
| Phase 0 | 环境搭建 + Hello Agent | Day 1-2 |
| Phase 1 | Function Calling | Day 3-4 |
| Phase 2-3 | Orchestrator + 专家 | Day 5-7 |
| Phase 4-5 | 后端 + 前端 | Day 8-10 |
| Phase 6 | 调试优化 | Day 11-12 |
| Phase 7 | 面试准备 | Day 13-14 |

## 🛠️ 技术栈

- **后端**: Python 3.11 + FastAPI + FastMCP
- **前端**: Vue3 + Vite + 高德地图JS API
- **LLM**: DeepSeek / OpenAI 兼容API
- **数据**: 高德地图 Web Service API

## 🎓 面试准备

完成本项目后，你将能够回答:

1. **架构设计**: 为什么选择Orchestrator-Workers模式？
2. **协议理解**: MCP解决了什么问题？
3. **工程实践**: 如何处理LLM幻觉？
4. **性能优化**: 如何减少Token消耗？

## 📖 参考资料

- [HelloAgents GitHub](https://github.com/datawhalechina/hello-agents)
- [FastMCP 文档](https://gofastmcp.com/)
- [高德地图API](https://lbs.amap.com/api/webservice/summary)
- [DeepSeek API](https://platform.deepseek.com/docs)

## 📄 License

MIT License - 可自由使用、修改、分发

---

**Happy Coding! 让我们一起构建智能的未来 🚀**
