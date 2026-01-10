# Day 8.2: 多日行程生成器 (Itinerary Generator) ⭐核心

## 🎯 学习目标
- [ ] 设计结构化的行程数据模型
- [ ] 实现多日行程生成逻辑
- [ ] 整合多 Agent 结果

---

## 1. 概念讲解

### 1.1 什么是多日行程方案？
用户输入 "北京3日游，喜欢历史" 后，系统应返回：
```json
{
  "city": "北京",
  "days": 3,
  "itinerary": [
    {
      "day": 1,
      "date": "2026-01-11",
      "weather": "晴, 5℃",
      "morning": [{"name": "故宫", "duration": "3h"}],
      "afternoon": [{"name": "天坛", "duration": "2h"}],
      "dinner": {"name": "全聚德", "type": "餐厅"},
      "hotel": {"name": "北京饭店", "rating": 4.8}
    },
    // Day 2, Day 3...
  ]
}
```

### 1.2 核心挑战
1. **工具编排**: 需要依次调用 Weather → Scout (景点) → Scout (餐厅) → Hotel
2. **时间安排**: 合理分配上午/下午活动
3. **天气适配**: 雨天推荐室内景点

---

## 2. 数据模型设计

### 2.1 Pydantic 模型
**文件**: `src/phase8/models.py`

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class POI(BaseModel):
    name: str
    address: Optional[str] = None
    rating: Optional[float] = None
    duration: Optional[str] = None  # 建议游玩时长
    location: Optional[str] = None  # 经纬度

class DayPlan(BaseModel):
    day: int = Field(description="第几天")
    date: Optional[str] = None
    weather: str = Field(description="天气预报")
    morning: List[POI] = Field(description="上午活动")
    afternoon: List[POI] = Field(description="下午活动")
    dinner: Optional[POI] = None
    hotel: Optional[POI] = None

class Itinerary(BaseModel):
    city: str
    days: int
    preferences: List[str] = []
    itinerary: List[DayPlan]
```

---

## 3. 生成器实现

### 3.1 核心逻辑
**文件**: `src/phase8/itinerary_generator.py`

```python
import asyncio
from typing import List
from src.phase3.tools import get_weather, search_poi
from src.phase8.models import Itinerary, DayPlan, POI

class ItineraryGenerator:
    def __init__(self):
        self.weather_cache = {}
    
    async def generate(self, city: str, days: int, preferences: List[str]) -> Itinerary:
        """生成多日行程"""
        # 1. 获取天气 (一次性获取多天预报)
        weather = await self._get_weather(city)
        
        # 2. 搜索景点
        attractions = await self._search_attractions(city, preferences)
        
        # 3. 搜索餐厅
        restaurants = await self._search_restaurants(city)
        
        # 4. 搜索酒店
        hotels = await self._search_hotels(city)
        
        # 5. 组装行程
        day_plans = []
        for d in range(1, days + 1):
            plan = DayPlan(
                day=d,
                weather=weather,
                morning=self._pick_pois(attractions, 2),
                afternoon=self._pick_pois(attractions, 1),
                dinner=self._pick_pois(restaurants, 1)[0] if restaurants else None,
                hotel=self._pick_pois(hotels, 1)[0] if hotels else None
            )
            day_plans.append(plan)
        
        return Itinerary(
            city=city,
            days=days,
            preferences=preferences,
            itinerary=day_plans
        )
    
    async def _get_weather(self, city: str) -> str:
        result = get_weather(city)
        return result
    
    async def _search_attractions(self, city: str, preferences: List[str]) -> List[POI]:
        keyword = preferences[0] if preferences else "景点"
        result = search_poi(city, keyword, "景点")
        # 解析结果为 POI 列表 (简化处理)
        return [POI(name=line.split(".")[1].strip().split("(")[0]) 
                for line in result.split("\n") if line]
    
    async def _search_restaurants(self, city: str) -> List[POI]:
        result = search_poi(city, "美食", "餐厅")
        return [POI(name=line.split(".")[1].strip().split("(")[0]) 
                for line in result.split("\n") if line]
    
    async def _search_hotels(self, city: str) -> List[POI]:
        result = search_poi(city, "酒店", "酒店")
        return [POI(name=line.split(".")[1].strip().split("(")[0]) 
                for line in result.split("\n") if line]
    
    def _pick_pois(self, pois: List[POI], count: int) -> List[POI]:
        """从列表中取出指定数量的 POI (避免重复)"""
        picked = pois[:count]
        for p in picked:
            if p in pois:
                pois.remove(p)
        return picked
```

---

## 4. 测试验证

```python
# test_itinerary.py
import asyncio
from src.phase8.itinerary_generator import ItineraryGenerator

async def main():
    gen = ItineraryGenerator()
    result = await gen.generate("北京", 3, ["历史"])
    print(result.model_dump_json(indent=2))

asyncio.run(main())
```

---

## 5. 面试要点
> 🗣️ "多日行程生成是本项目的核心亮点。我使用 Pydantic 定义了 `DayPlan` 结构化模型，通过编排 Weather/Scout/Hotel 三个 Agent 获取数据源，然后按照智能时间分配算法填充每天的活动。这体现了 Agentic Workflow 的'规划-执行-整合'三阶段范式。"
