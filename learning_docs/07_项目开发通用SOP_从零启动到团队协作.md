# 07 项目开发通用 SOP：从零启动到团队协作 🚀

> **文档定位**: 这是你的“编程生存手册”。无论是自己开新项目，还是加入别人的项目，只要按着这个流程走，就能避开 90% 的环境和 Git 坑。

---

## 🛠️ 第一阶段：准备工作 (所有项目的基石)

### 1. 核心工具检查
*   **终端必须用**: **Git Bash** (拒绝 PowerShell/CMD，避免乱码和语法报错)。
*   **Python 版本**: 确认安装了 Python 3.10+ (`python --version`)。
*   **编辑器**: VS Code (推荐安装 Python 和 Markdown All in One 插件)。

### 2. API 密钥准备 (你的通行证)
不要每次都临时去找，把它们保存在安全的地方（如密码管理器）。
*   **DeepSeek (LLM)**: 
    *   获取地址: [DeepSeek 开放平台](https://platform.deepseek.com/api_keys)
    *   格式: `sk-xxxx...`
*   **高德地图 (Amap)**:
    *   获取地址: [高德控制台](https://console.amap.com/dev/key/app)
    *   应用类型: **Web服务** (不是 Web端/JSAPI)
    *   关键信息: `Key` (必填)

---

## 🚦 第二阶段：启动项目 (两种情况)

### 情况 A：我是发起人 (新建空项目)

**目标**: 从零开始，搭建地基。

1.  **创建目录**:
    ```bash
    mkdir my-new-project
    cd my-new-project
    ```
2.  **初始化 Git**:
    ```bash
    git init
    ```
3.  **创建忽略文件 (必须先做!)**:
    > 防止把环境和私钥传上去。
    ```bash
    touch .gitignore
    # 编辑它，写入:
    # venv/
    # .env
    # __pycache__/
    ```
4.  **搭建 Python 环境**:
    ```bash
    python -m venv venv           # 造房间
    source venv/Scripts/activate  # 进房间 (Git Bash 写法)
    ```
5.  **配置密钥**:
    ```bash
    touch .env
    # 编辑写入: DEEPSEEK_API_KEY=sk-xxx...
    ```

### 情况 B：我是加入者 (基于现有 GitHub 项目)

**目标**: 拉取别人的代码，在自己电脑跑起来。

1.  **拉取代码 (Clone)**:
    ```bash
    # 复制 GitHub 上的 HTTPS 地址
    git clone https://github.com/username/project-name.git
    cd project-name
    ```
2.  **搭建 Python 环境**:
    ```bash
    # 即使代码里有 venv 文件夹，你也要自己重建，因为 venv 不跨电脑
    python -m venv venv
    source venv/Scripts/activate
    ```
3.  **安装依赖 (还原现场)**:
    > 这一步是为了让你的环境和作者一模一样。
    ```bash
    pip install -r requirements.txt
    ```
4.  **配置密钥**:
    > 别人的代码里一定没有 .env (因为被忽略了)，你需要自己建。
    *   通常作者会留一个 `.env.example`。
    *   `cp .env.example .env` (复制一份)。
    *   填入你自己的 Key。

---

## 🔄 第三阶段：日常开发循环 (SOP)

**口诀**: **切分支 -> 写代码 -> 测代码 -> 传代码 -> 提合并**

### 1. 开始工作前
*   **永远不要在 main 分支直接改代码！**
*   **同步最新状态**:
    ```bash
    git checkout main
    git pull origin main
    ```

### 2. 这里的开发流程
*   **创建任务分支**:
    *   命名规范: `feature/功能名` 或 `fix/bug名`
    *   命令: `git checkout -b feature/add-login`
*   **写代码 & 运行**:
    *   记得激活环境: `source venv/Scripts/activate`
    *   运行代码测试: `python src/main.py`

### 3. 保存与上传
*   **保存现场**:
    ```bash
    git add .
    git commit -m "feat: 实现了登录功能"
    ```
*   **推送到云端**:
    ```bash
    git push origin feature/add-login
    ```

### 4. 提交合并 (Pull Request)
*   打开 GitHub 页面。
*   点击 "Compare & pull request"。
*   等待合并。

---

## 🛑 第四阶段：避坑指南 (血泪教训)

1.  **报错: `Scripts execution policy...` 或 `&&` 错误**:
    *   ❌ **原因**: 用了 PowerShell。
    *   ✅ **解法**: 马上切换到 **Git Bash**。

2.  **报错: `No module named 'xxx'`**:
    *   ❌ **原因**: 没激活虚拟环境，或者没装包。
    *   ✅ **解法**: 
        1. 看命令行前有没有 `(venv)`？没有就 `source venv/Scripts/activate`。
        2. 运行 `pip install -r requirements.txt`。

3.  **乱码**:
    *   ❌ **原因**: Windows 中文编码问题。
    *   ✅ **解法**: `.gitignore` 和代码文件里尽量用英文注释；坚持用 Git Bash。

4.  **API 报错 (401 Unauthorized)**:
    *   ❌ **原因**: Key 填错了，或者余额不足。
    *   ✅ **解法**: 检查 `.env` 文件，确认没有多余空格；去官网后台看余额。

---

**保存这份文档，下次开新项目时，对照执行即可！** 🌟
