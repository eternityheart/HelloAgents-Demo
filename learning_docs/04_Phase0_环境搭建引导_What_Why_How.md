# 04 Phase 0 环境搭建引导 (What, Why, How)

> **导语**: 欢迎开始第一步！在写任何智能代码之前，我们需要先搭建一个“坚固的地基”。不要小看这一步，很多初学者的挫败感都来自环境配置问题。跟着我，一步步稳稳地来。

## 🔍 What: 我们要创建什么？

在这一阶段，我们主要完成三件事：
1.  **Python 虚拟环境 (`venv`)**: 一个独立的、干净的“房间”，专门用来放这个项目的工具包。
2.  **环境变量文件 (`.env`)**: 一个安全的“保险箱”，用来存放你的 API 密钥（DeepSeek, 高德地图等），不让别人看见。
3.  **Hello World Agent**: 一个最简单的 AI 机器人，用来测试你的环境和密钥是否工作正常。

## 🤔 Why: 为什么要这么做？

你可能会问：*“我直接 pip install 不行吗？为什么要搞这么复杂？”*

1.  **为什么要虚拟环境？**
    *   想象一下，你的电脑是你的家。如果不分开，所有的项目（客人）都挤在客厅里。A项目要用旧版工具，B项目要用新版工具，它们就会打架（版本冲突）。
    *   **虚拟环境**就是给HelloAgents项目单独开一个房间，它想怎么乱搞都不会影响其他项目，也不会被其他项目影响。这是**专业工程师的第一课**。

2.  **为什么要环境变量？**
    *   你的 API Key 就像银行卡密码。如果你把它直接写在代码里（Hardcode），一旦你把代码分享给别人或上传到 GitHub，全世界都能以此花你的钱。
    *   **`.env` 文件**通常会被忽略（即不上传），代码通过读取环境变量来获取密码。这样代码是公开的，但密码是安全的。

3.  **为什么要先做 Hello World？**
    *   在造火箭之前，先点根火柴试试。如果连最简单的对话都跑不通，后面复杂的Agent更无从谈起。这是**最小可行性测试 (MVP)** 的思维。

## 🛠️ How: 如何搭建起来？

请打开你的终端（Terminal/PowerShell），跟着我敲命令。

### Step 1: 创建独立的“房间” (虚拟环境)

```powershell
# 1. 确保你在项目根目录下
cd e:\antiPro\agentdemo1

# 2. 创建虚拟环境 (名字叫 venv)
python -m venv venv

# 3. 激活环境 (进入房间)
# 如果成功，你的命令行前面会出现 (venv) 字样
venv\Scripts\activate
```

### Step 2: 安装必要的“家具” (依赖包)

```powershell
# 安装 requirements.txt 里列出的所有包
pip install -r requirements.txt
```

*如果下载慢，可以使用清华源加速：*
`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

### Step 3: 设置“保险箱” (环境变量)

1.  找到项目目录下的 `.env.example` 文件。
2.  把它复制一份，重命名为 `.env`。
3.  用文本编辑器打开 `.env`，填入你的密钥：

```ini
# DeepSeek API Key (去 https://platform.deepseek.com 申请)
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx

# 高德地图 Key (去 https://console.amap.com 申请 Web服务Key)
AMAP_API_KEY=xxxxxxxxxxxxxxxx
```

### Step 4: 点火测试 (Hello World)

```powershell
# 运行第一个测试脚本
python src/phase0_hello_agent.py
```

**🎉 成功标志**:
如果你看到屏幕上出现：
`✅ Agent已就绪! 试着问我一些旅行问题吧~`
并且你能跟它对话，恭喜你！地基已经打好了！

---

### 👉 下一步
当你完成以上步骤后，请告诉我“环境搭建完成”，我们将进入 **Phase 1: 核心概念理解**，去拆解 Agent 到底是怎么思考的。
