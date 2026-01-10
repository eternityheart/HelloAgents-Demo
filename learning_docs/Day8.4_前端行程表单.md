# Day 8.4-8.5: 前端行程表单与后端 API

## 🎯 学习目标
- [ ] 添加行程规划表单界面
- [ ] 实现 `/api/itinerary` 后端接口
- [ ] 前后端联调测试

---

## 1. 前端行程表单 (8.4)

### 1.1 HTML 结构
在 `index.html` 中添加"规划模式"切换：

```html
<!-- 模式切换 -->
<div class="mode-toggle">
    <button id="chatModeBtn" class="active">💬 对话模式</button>
    <button id="planModeBtn">📋 规划模式</button>
</div>

<!-- 行程规划表单 (默认隐藏) -->
<div id="planForm" class="plan-form hidden">
    <h3>🗺️ 行程规划</h3>
    <div class="form-group">
        <label>目的地</label>
        <input type="text" id="destinationInput" placeholder="例如: 北京">
    </div>
    <div class="form-group">
        <label>天数</label>
        <select id="daysSelect">
            <option value="1">1天</option>
            <option value="2">2天</option>
            <option value="3" selected>3天</option>
            <option value="5">5天</option>
            <option value="7">7天</option>
        </select>
    </div>
    <div class="form-group">
        <label>偏好标签</label>
        <div class="tags">
            <label><input type="checkbox" value="历史"> 历史</label>
            <label><input type="checkbox" value="美食"> 美食</label>
            <label><input type="checkbox" value="自然"> 自然</label>
            <label><input type="checkbox" value="购物"> 购物</label>
        </div>
    </div>
    <button id="generateBtn" class="generate-btn">🚀 生成行程</button>
</div>
```

### 1.2 CSS 样式
```css
.plan-form {
    padding: 20px;
    background: var(--card-bg);
    border-radius: 16px;
}
.plan-form.hidden { display: none; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; margin-bottom: 8px; color: var(--doraemon-blue); }
.form-group input, .form-group select {
    width: 100%;
    padding: 12px;
    border: 2px solid var(--card-border);
    border-radius: 8px;
}
.tags label { margin-right: 12px; }
.generate-btn {
    width: 100%;
    padding: 14px;
    background: var(--doraemon-blue);
    color: white;
    border: none;
    border-radius: 25px;
    font-size: 1rem;
    cursor: pointer;
}
```

### 1.3 JavaScript 逻辑
```javascript
// 模式切换
chatModeBtn.onclick = () => {
    planForm.classList.add('hidden');
    chatSection.classList.remove('hidden');
};
planModeBtn.onclick = () => {
    chatSection.classList.add('hidden');
    planForm.classList.remove('hidden');
};

// 生成行程
generateBtn.onclick = async () => {
    const destination = destinationInput.value;
    const days = parseInt(daysSelect.value);
    const preferences = [...document.querySelectorAll('.tags input:checked')]
        .map(c => c.value);
    
    const response = await fetch('/api/itinerary', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ destination, days, preferences })
    });
    
    const data = await response.json();
    displayItinerary(data);
};
```

---

## 2. 后端行程 API (8.5)

### 2.1 API 模型
**文件**: `src/phase6/api_models.py`

```python
from pydantic import BaseModel
from typing import List

class ItineraryRequest(BaseModel):
    destination: str
    days: int = 3
    preferences: List[str] = []
```

### 2.2 API 端点
**文件**: `src/phase6/main.py`

```python
from src.phase8.itinerary_generator import ItineraryGenerator

generator = ItineraryGenerator()

@app.post("/api/itinerary")
async def create_itinerary(request: ItineraryRequest):
    """生成多日行程"""
    result = await generator.generate(
        city=request.destination,
        days=request.days,
        preferences=request.preferences
    )
    return result.model_dump()
```

---

## 3. 验收标准
- [ ] 前端表单可切换显示
- [ ] 提交后调用 API 成功
- [ ] 返回结构化行程 JSON
- [ ] 界面展示多日行程卡片

---

## 4. 面试要点
> 🗣️ "前端我采用了模式切换设计，用户可以选择'对话模式'进行自由提问，或切换到'规划模式'通过表单精确输入需求。后端 FastAPI 接收结构化请求，调用 ItineraryGenerator 生成行程，返回 Pydantic 模型确保数据一致性。这种设计兼顾了灵活性和精确性。"
