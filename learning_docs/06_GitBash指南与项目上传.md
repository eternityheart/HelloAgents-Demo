# 06 Git Bash 使用指南与项目上传 (解决乱码与报错)

> **为什么你会遇到 `&&` 报错？**
> 在 Windows 的默认终端 (PowerShell) 中，语句连接符是 `;` 而不是 `&&`。但为了和全球开发者统一口径（Linux/Mac 教程都用 `&&`），我们强烈推荐你通过 **Git Bash** 来执行 Git 命令。

## 1. 切换到 Git Bash (强烈推荐)

我们在安装 Git 时通常都自动安装了 **Git Bash**。
1.  在你的项目文件夹 (`e:\antiPro\agentdemo1`) 空白处，**右键单击**。
2.  选择 "**Open Git Bash here**" (如果没有，请在开始菜单搜索 Git Bash 打开，然后用 `cd` 命令进入目录)。
3.  你会看到一个彩色的命令行窗口，这就是你的“专业开发者控制台”。

---

## 2. HelloAgents-Demo 项目上传实战

请在 **Git Bash** 中依次复制并运行以下命令（不用担心报错，这里支持 `&&`）：

### 第一步：告诉 Git 你是谁 (如果还没设置过)
```bash
git config --global user.name "eternityheart"
git config --global user.email "你的邮箱@example.com"
```

### 第二步：提交本地代码
```bash
# 1. 初始化仓库 (如果之前没成功)
git init

# 2. 添加所有文件 (注意有个点)
git add .

# 3. 提交到本地仓库
git commit -m "first commit: HelloAgents environment setup"
```

### 第三步：推送到 GitHub
```bash
# 1. 关联远程仓库 (请确保这是你刚才创建的地址)
git remote add origin https://github.com/eternityheart/HelloAgents-Demo.git

# 2. 重命名主分支为 main (符合现代标准)
git branch -M main

# 3. 推送! (这一步可能需要你浏览器授权)
git push -u origin main
```

---

## 3. 未来的分支管理规范 (SOP)

当项目成功上传后，以后的开发请遵循以下流程：

### 🌳 情况 A：开发新功能 (比如 Day 5 的后端开发)

1.  **打开 Git Bash**
2.  **拉取最新代码** (防止冲突):
    ```bash
    git checkout main && git pull origin main
    ```
3.  **创建新分支**:
    ```bash
    git checkout -b feature/backend-basic
    ```
4.  **写代码...**
5.  **提交与上传**:
    ```bash
    git add .
    git commit -m "feat: setup fastapi basic structure"
    git push origin feature/backend-basic
    ```
6.  **去 GitHub 提 Pull Request 合并**

### 🐛 情况 B：修复 Bug

1.  **创建修复分支**:
    ```bash
    git checkout -b fix/utf8-encoding-error
    ```
2.  **修复代码...**
3.  **提交与上传**:
    ```bash
    git add .
    git commit -m "fix: resolve encoding issue in requirements.txt"
    git push origin fix/utf8-encoding-error
    ```

---

## 💡 总结
*   **报错原因**: PowerShell 不认 `&&`。
*   **解决方案**: 用 **Git Bash**。
*   **核心习惯**: `git add .` -> `git commit` -> `git push`。
