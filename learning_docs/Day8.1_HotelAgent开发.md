# Day 8.1: 酒店推荐 Agent 开发 (Hotel Agent)

## 🎯 学习目标
- [ ] 理解 POI 类型代码与酒店搜索
- [ ] 创建独立的 Hotel Agent
- [ ] 注册为 MCP 工具

---

## 1. 概念讲解

### 1.1 为什么需要专门的酒店 Agent？
虽然 Scout Agent 已经可以搜索酒店 POI，但专门的 Hotel Agent 有以下优势：
- **参数专业化**: 酒店特有的筛选条件（价格区间、星级）
- **结果格式化**: 返回酒店专属信息（房价、设施）
- **职责清晰**: Orchestrator 调度时语义更明确

### 1.2 高德酒店 POI 类型代码
```python
POI_TYPES = {
    "酒店": "100000",      # 一级分类
    "星级酒店": "100100",  # 五星/四星
    "经济型酒店": "100200",
    "公寓式酒店": "100300"
}
```

---

## 2. 代码实现

### 2.1 Hotel Agent 核心逻辑
**文件**: `src/phase4/hotel_agent.py`

```python
from fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv

mcp = FastMCP("Hotel Agent")
load_dotenv()
AMAP_API_KEY = os.getenv("AMAP_API_KEY")

@mcp.tool(description="搜索酒店，支持价格和评分筛选")
def search_hotel(
    city: str, 
    keyword: str = "酒店", 
    min_rating: float = 4.0,
    max_results: int = 5
) -> str:
    """
    搜索酒店
    
    Args:
        city: 城市名称
        keyword: 搜索关键词 (默认"酒店")
        min_rating: 最低评分 (默认4.0)
        max_results: 返回数量
    """
    url = "https://restapi.amap.com/v3/place/text"
    resp = requests.get(url, params={
        "key": AMAP_API_KEY,
        "city": city,
        "keywords": keyword,
        "types": "100000",  # 酒店类型
        "citylimit": "true",
        "offset": max_results * 2  # 多请求一些，后续过滤
    }, proxies={"http": None, "https": None}, timeout=5)
    
    data = resp.json()
    if data["status"] != "1":
        return f"API错误: {data.get('info')}"
    
    results = []
    for poi in data.get("pois", []):
        rating = float(poi.get("biz_ext", {}).get("rating", "0") or "0")
        if rating >= min_rating:
            results.append({
                "name": poi.get("name"),
                "address": poi.get("address"),
                "rating": rating,
                "tel": poi.get("tel"),
                "location": poi.get("location")
            })
        if len(results) >= max_results:
            break
    
    if not results:
        return f"未找到评分高于 {min_rating} 的酒店"
    
    # 格式化输出
    output = []
    for i, h in enumerate(results, 1):
        output.append(f"{i}. {h['name']} (评分:{h['rating']}) - {h['address']}")
    return "\n".join(output)

if __name__ == "__main__":
    mcp.run()
```

---

## 3. 测试验证

### 3.1 直接测试脚本
```python
# test_hotel_direct.py
from hotel_agent import search_hotel

result = search_hotel("北京", "五星级酒店", min_rating=4.5)
print(result)
```

### 3.2 验收标准
- [ ] 能搜索指定城市的酒店
- [ ] 能按评分过滤结果
- [ ] 返回格式包含名称、地址、评分

---

## 4. 面试要点
> 🗣️ "我将酒店搜索独立为专门的 Agent，遵循单一职责原则。通过 MCP 协议注册后，Orchestrator 可以根据用户意图自动调度。这种解耦设计便于后续扩展（如接入携程API）。"
