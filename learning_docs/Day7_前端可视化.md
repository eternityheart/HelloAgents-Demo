# Day 7: 前端可视化与交互实现

## 🎯 学习目标
- [ ] 掌握基于 CSS 变量的主题定制 (Doraemon Theme)
- [ ] 实现沉浸式对话 UI (头像、气泡、打字机效果)
- [ ] 集成高德地图 JS API (定位、搜索、路径规划)
- [ ] 实现前端状态持久化 (LocalStorage)

---

## 1. 🎨 哆啦A梦主题 UI 系统
我们不使用沉重的 UI 框架，而是手写了一套轻量级的 CSS 主题系统。

### 1.1 核心配色 (`doraemon.css`)
利用 CSS 变量实现全局统一样式控制：
```css
:root {
    /* 核心角色色 */
    --doraemon-blue: #00a0e9;   /* 哆啦A梦蓝 */
    --nobita-yellow: #ffd700;   /* 大雄黄 (工作状态) */
    --shizuka-pink: #ffb6c1;    /* 静香粉 */
    
    /* 玻璃拟态 (Glassmorphism) */
    --card-bg: rgba(255, 255, 255, 0.85);
    --card-border: rgba(0, 160, 233, 0.3);
}
```
**实现原理**:
- **背景**: 多层背景叠加。底层是图片(`bg_doraemon_1.jpg`)，上层是半透明渐变遮罩(`linear-gradient`)，保证文字可读性。
- **卡片**: 使用 `backdrop-filter: blur(10px)` 产生毛玻璃效果，配合半透明白色背景。

### 1.2 沉浸式对话布局
为了模拟真实聊天体验，我们实现了分侧布局：

**HTML 结构 (`index.html`)**:
- 容器使用 `.chat-messages` (Flex column)
- 单条消息使用 `.message-row` (Flex row)

**CSS 技巧 (`doraemon.css`)**:
```css
/* 大雄 (用户) - 右侧 */
.message-row.user {
    align-self: flex-end;
    flex-direction: row-reverse; /* 头像在最右 */
}

/* 哆啦A梦 (Agent) - 左侧 */
.message-row.agent {
    align-self: flex-start;
}
```
配合 `app.js` 动态地根据 `type` 选择头像图片 (`nobita.png` vs `doraemon.png`)。

---

## 2. 🗺️ 高德地图深度集成 (`map.html`)
不仅仅是展示地图，我们打造了一个完整的路径规划控制台。

### 2.1 三栏式布局设计
- **左栏 (控制)**: 起终点输入、当前定位、图例
- **中栏 (地图)**: 核心交互区，保持正方形比例
- **右栏 (数据)**: 实时计算的路线数据（距离、时间）

### 2.2 核心功能实现
所有地图逻辑封装在 `map.html` 的 `<script>` 标签中。

#### A. 📍 智能定位 (Location)
优先使用浏览器原生 API，失败则回退。
```javascript
// 核心逻辑: tryBrowserGeolocation -> fallbackLocation
navigator.geolocation.getCurrentPosition(
    (pos) => { /* 成功: 使用精确坐标 */ },
    (err) => { /* 失败: 使用默认坐标(北京) */ }
);
```

#### B. 🔍 自动补全 (Autocomplete)
让输入像原生 App 一样顺滑：
```javascript
// 引入插件
AMap.plugin('AMap.AutoComplete', function() {
    var auto = new AMap.AutoComplete({ input: "startInput" });
    // 监听选择事件
    auto.on("select", select); 
});
```

#### C. 🛣️ 双色路径规划 (Comparison)
我们同时展示 **步行** 和 **驾车** 方案进行对比：

1. **API 调用**: 同时发起 `walking.search()` 和 `driving.search()`
2. **自定义绘制**: 
   - 隐藏默认路线 (`map: null`)
   - 提取路径坐标 (`steps.path`)
   - **手动绘制**:
     - 🚶 **步行**: 蓝色 Polyline (`#2196F3`), 虚线或实线
     - 🚗 **驾车**: 红色 Polyline (`#F44336`)
3. **数据计算**:
   - `result.routes[0].distance` (米)
   - `result.routes[0].time` (秒)
   - 直线距离: `AMap.GeometryUtil.distance`

---

## 3. 🧠 状态管理与持久化 (`app.js`)

### 3.1 聊天记录漫游
为了让用户在 "聊天页" 和 "地图页" 切换时不丢失上下文：

1. **保存**: 每次 `addMessage` 时，同步写入 `localStorage`
   ```javascript
   localStorage.setItem('chat_history', JSON.stringify(chatHistory));
   ```
2. **加载**: 页面 `onload` 时读取并渲染
   ```javascript
   const saved = localStorage.getItem('chat_history');
   if (saved) chatHistory = JSON.parse(saved);
   ```

### 3.2 SSE 流式响应处理
前端如何优雅地处理 LLM 的打字机效果？

1. **Fetch**: 发起 POST 请求
2. **Stream Reader**: 使用 `response.body.getReader()`
3. **Decoder**: `new TextDecoder()` 逐块解码
4. **Buffer**: 处理被切断的 JSON 行
5. **UI Update**: 实时追加文本内容 (`lastMsg.textContent += data`)

---

## 4. 📝 交付物清单
- `src/phase7/index.html`: 聊天主入口
- `src/phase7/map.html`: 地图功能页
- `src/phase7/doraemon.css`: 自定义主题样式表
- `src/phase7/app.js`: 前端核心逻辑
- `src/phase7/assets/`: 图片资源 (哆啦A梦, 大雄, 静香, 背景图)

## 5. 面试重点
> 🗣️ "在这个阶段，我不仅实现了功能，更注重 **用户体验 (UX)**。
> 1. **视觉反馈**: 通过头像和气泡区分角色，使用 SSE 打字机减少等待焦虑。
> 2. **容错性**: 地图定位包含完整的 Fallback 机制。
> 3. **状态连续性**: 利用 LocalStorage 实现了简单的状态管理，避免页面刷新导致的数据丢失。
> 这展示了我对完整 Web 应用开发流程的把控能力。"
