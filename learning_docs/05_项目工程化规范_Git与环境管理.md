# 项目工程化规范：环境与版本控制 (SOP)

> **文档目标**: 这是一份标准操作流程 (SOP)。以后每当你开启一个新项目（无论是 AI Agent 还是 Web 应用），都请严格按照本指南操作。这能让你从“写代码的学生”转变为“管理项目的工程师”。

---

## 1. 环境管理规范 (Environment)

**核心原则**: 每个项目必须有独立的“房间”（虚拟环境）和“保险箱”（密钥管理）。

### 🟢 启动新项目标准动作
每当你创建一个新文件夹（例如 `my_new_project`）准备开始写代码时：

1.  **造房间 (venv)**:
    ```bash
    # 在项目根目录下运行
    python -m venv venv
    ```
2.  **进房间 (Activate)**:
    ```bash
    # Windows
    venv\Scripts\activate
    # 成功标志: 命令行前出现 (venv)
    ```
3.  **设忽略 (.gitignore)**:
    *   **必须做**: 在写第一行代码前，先创建 `.gitignore` 文件。
    *   **写入**: `venv/`, `.env`, `__pycache__/`。
    *   **目的**: 即使你不小心提交，Git 也会拦住你，不把垃圾文件和密钥传上去。
4.  **配保险 (.env)**:
    *   复制 `.env.example` 为 `.env`。
    *   填入 API Key。
    *   永远不要把 `.env` 提交到 Git（全靠 .gitignore 保护）。

### 📚 依赖管理
*   **安装包**:必须在 `(venv)` 状态下 `pip install xxx`。
*   **留配方**: 每次装完新包，**立即**运行：
    ```bash
    pip freeze > requirements.txt
    ```
    这样别人（或未来的你）才能复现你的环境。

---

## 2. Git 版本控制规范

**核心原则**: 不要直接在 `main` 主分支上写代码。主分支是神圣的，只能通过合并（Merge）进入。

### 🌳 分支管理策略 (Branching Model)

我们采用轻量级的 **Feature Branch Workflow**：

1.  **`main` (主分支)**:
    *   **状态**: 永远是可运行的、稳定的。
    *   **操作**: **严禁**直接 Push 代码。只能接受来自其他分支的合并。
2.  **`dev` (开发主分支/集成分支)**: (可选，大项目推荐)
    *   **状态**: 这是大家平时“交作业”的地方，可能偶尔会有 Bug。
    *   **操作**: 日常开发的基础分支。
3.  **`feature/xxx` (功能分支)**:
    *   **状态**: 你的“平行宇宙”，你可以随便折腾。
    *   **命名**: `feature/login` (做登录), `feature/agent-ui` (做UI), `fix/bug-1` (修Bug)。
    *   **生命周期**: 开发完 -> 合并回 dev -> 删除。

### 🔄 日常开发工作流 (The Cycle)

假设你要开始做一个新功能“添加天气查询”：

**Step 1: 切分支 (Start)**
```bash
# 1. 确保在最新的主分支上
git checkout main
git pull origin main

# 2. 创建并切换到新分支
git checkout -b feature/weather-tool
```

**Step 2: 写代码 (Work)**
*   写代码... 测试...
*   **提交**: 
    ```bash
    git add .
    git commit -m "feat: 完成天气查询工具的基本逻辑"
    ```

**Step 3: 交作业 (Upload)**
```bash
# 把你的平行宇宙推送到云端
git push origin feature/weather-tool
```

**Step 4: 申请合并 (Pull Request / PR)**
*   **你的动作**: 打开 GitHub 网页。
*   **GitHub**: 会提示你“feature/weather-tool had recent pushes”。
*   **点击**: `Compare & pull request`。
*   **填写**: 说明你做了什么。
*   **点击**: `Create pull request`。

**Step 5: 验收与合并 (Merge)**
*   自己（或同事）Review 代码。
*   点击 `Merge pull request` -> `Confirm merge`。
*   GitHub 会把你的代码合并进 `main`。
*   **本地收尾**:
    ```bash
    git checkout main
    git pull origin main  # 把云端合并好的代码拉回来
    ```

---

## 3. GitHub 交互指南 (Project Setup)

这部分是你在**这步**（项目初始化时）必须配合的操作。

### 🤝 需要你配合的动作

AI 无法帮你点击 GitHub 网页上的按钮，也无法输入你的密码。以下步骤需要你亲自完成：

1.  **去 GitHub 创建仓库**:
    *   登录 GitHub。
    *   点右上角 `+` -> `New repository`。
    *   Repository name: `HelloAgents-Demo` (或者你喜欢的名字)。
    *   **不要勾选** "Initialize with README/gitignore" (因为我们本地已经有了)。
    *   点击 `Create repository`。
2.  **获取仓库地址**:
    *   创建成功后，复制那个 HTTPS 地址 (例如: `https://github.com/yourname/HelloAgents-Demo.git`)。
3.  **告诉我地址**:
    *   回到对话框，把地址发给我。

### 🤖 我会帮你做的动作

一旦你给了我地址，我会执行：

```bash
# 关联远程仓库
git remote add origin <你的地址>

# 第一次推送 (把本地现在的这些代码推上去)
git branch -M main
git push -u origin main
```

---

## ✅ 总结：下一次开新项目怎么做？

1.  `mkdir new_project` & `cd`
2.  `python -m venv venv`
3.  `git init`
4.  创建 `.gitignore`
5.  在 GitHub 建仓库，拿到 URL
6.  `git remote add origin URL`
7.  `git checkout -b feature/setup` -> 开始写代码！
