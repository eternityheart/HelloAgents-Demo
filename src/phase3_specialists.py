"""
Phase 3: 专家Agents - 功能型Agent与MCP封装

🧒 小学生讲解:
现在我们的"旅行社"要招聘专家了！
之前只有一个"万能员工"，什么都做但不够专业。
现在我们要招3个专家：
  - 🔭 Scout（侦察兵）：专门找景点
  - 🌤️ Meteorologist（气象员）：专门查天气
  - 🏨 Concierge（礼宾员）：专门找酒店和餐厅

每个专家只做自己擅长的事，效率更高！

学习目标:
1. 理解职责分离（Separation of Concerns）
2. 学会用FastMCP封装工具
3. 理解MCP的Client-Server架构

🎓 面试话术:
"我将系统拆分为多个专家Agent，每个负责特定领域。
通过FastMCP封装为MCP服务器，实现工具的标准化与解耦。
这符合单一职责原则，也方便后续独立扩展和测试。"
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import os
import httpx
from dotenv import load_dotenv

load_dotenv()


# ===== 通用基类 =====

class BaseAgent:
    """
    专家Agent基类
    
    所有专家Agent都继承这个类，共享配置加载逻辑
    """
    def __init__(self):
        self.amap_key = os.getenv("AMAP_API_KEY", "")
        if not self.amap_key:
            print("⚠️ 警告: 未配置 AMAP_API_KEY，将使用模拟数据")


# ===== 数据模型 =====

class POIResult(BaseModel):
    """景点搜索结果"""
    name: str = Field(description="景点名称")
    address: str = Field(description="地址")
    location: str = Field(description="经纬度坐标")
    type: str = Field(description="类型分类")
    rating: Optional[float] = Field(default=None, description="评分")
    tel: Optional[str] = Field(default=None, description="电话")

class WeatherResult(BaseModel):
    """天气查询结果"""
    city: str
    weather: str
    temperature: str
    humidity: str
    wind: str
    report_time: str

class HotelResult(BaseModel):
    """酒店搜索结果"""
    name: str
    address: str
    location: str
    rating: Optional[float] = None
    price_range: Optional[str] = None


# ===== Scout Agent（侦察兵 - 景点搜索）=====

class ScoutAgent(BaseAgent):
    """
    侦察兵Agent - 专门负责搜索景点信息
    
    🧒 小学生讲解:
    侦察兵的工作就是帮你"踩点"，找到城市里有什么好玩的地方。
    他会告诉你：景点名字、地址、在哪里（坐标）、评分多少。
    """
    
    AMAP_POI_SEARCH_URL = "https://restapi.amap.com/v3/place/text"
    
    # 模拟数据（API未配置时使用）
    MOCK_DATA = {
        "北京": [
            POIResult(name="故宫博物院", address="北京市东城区景山前街4号", 
                     location="116.397026,39.918058", type="风景名胜", rating=4.8),
            POIResult(name="天坛公园", address="北京市东城区天坛路", 
                     location="116.410886,39.881933", type="风景名胜", rating=4.7),
            POIResult(name="颐和园", address="北京市海淀区新建宫门路19号", 
                     location="116.275191,39.999814", type="风景名胜", rating=4.6),
        ],
        "上海": [
            POIResult(name="外滩", address="上海市黄浦区中山东一路", 
                     location="121.490317,31.240018", type="风景名胜", rating=4.7),
            POIResult(name="东方明珠", address="上海市浦东新区世纪大道1号", 
                     location="121.499718,31.239703", type="风景名胜", rating=4.5),
        ]
    }
    
    async def search_attractions(
        self, 
        city: str, 
        keyword: str = "景点",
        limit: int = 5
    ) -> List[POIResult]:
        """
        搜索城市景点
        
        Args:
            city: 城市名称
            keyword: 搜索关键词
            limit: 返回结果数量
            
        Returns:
            景点列表
        """
        print(f"🔭 Scout: 在{city}搜索'{keyword}'...")
        
        # 如果没有API Key，使用模拟数据
        if not self.amap_key:
            mock_results = self.MOCK_DATA.get(city, [])[:limit]
            print(f"   📦 返回{len(mock_results)}个模拟结果")
            return mock_results
        
        # 调用真实API
        params = {
            "key": self.amap_key,
            "keywords": keyword,
            "city": city,
            "citylimit": "true",
            "extensions": "all",  # 获取详细信息
            "offset": limit,
            "output": "json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.AMAP_POI_SEARCH_URL, params=params)
            data = response.json()
        
        if data.get("status") != "1":
            print(f"   ❌ API错误: {data.get('info')}")
            return []
        
        # 解析结果
        results = []
        for poi in data.get("pois", []):
            results.append(POIResult(
                name=poi.get("name", ""),
                address=poi.get("address", ""),
                location=poi.get("location", ""),
                type=poi.get("type", "").split(";")[0] if poi.get("type") else "",
                rating=float(poi.get("biz_ext", {}).get("rating", 0)) or None,
                tel=poi.get("tel", "") or None
            ))
        
        print(f"   ✅ 找到{len(results)}个结果")
        return results


# ===== Meteorologist Agent（气象员 - 天气查询）=====

class MeteorologistAgent(BaseAgent):
    """
    气象员Agent - 专门负责查询天气信息
    
    🧒 小学生讲解:
    气象员的工作是告诉你"明天穿什么衣服"。
    他会查天气预报，告诉你温度、是否下雨、刮不刮风。
    """
    
    AMAP_WEATHER_URL = "https://restapi.amap.com/v3/weather/weatherInfo"
    
    # 模拟数据
    MOCK_DATA = {
        "北京": WeatherResult(city="北京", weather="晴", temperature="25", 
                             humidity="40%", wind="东北风3级", report_time="2024-01-01 10:00"),
        "上海": WeatherResult(city="上海", weather="多云", temperature="28",
                             humidity="65%", wind="东风2级", report_time="2024-01-01 10:00"),
        "广州": WeatherResult(city="广州", weather="小雨", temperature="30",
                             humidity="80%", wind="南风4级", report_time="2024-01-01 10:00"),
    }
    
    async def get_weather(self, city: str) -> WeatherResult:
        """
        获取城市天气
        
        Args:
            city: 城市名称
            
        Returns:
            天气信息
        """
        print(f"🌤️ Meteorologist: 查询{city}天气...")
        
        # 如果没有API Key，使用模拟数据
        if not self.amap_key:
            mock_result = self.MOCK_DATA.get(
                city, 
                WeatherResult(city=city, weather="未知", temperature="--",
                             humidity="--", wind="--", report_time="--")
            )
            print(f"   📦 返回模拟数据")
            return mock_result
        
        # 调用真实API
        params = {
            "key": self.amap_key,
            "city": city,
            "extensions": "base",
            "output": "json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.AMAP_WEATHER_URL, params=params)
            data = response.json()
        
        if data.get("status") != "1":
            print(f"   ❌ API错误: {data.get('info')}")
            return WeatherResult(city=city, weather="查询失败", temperature="--",
                                humidity="--", wind="--", report_time="--")
        
        live = data.get("lives", [{}])[0]
        result = WeatherResult(
            city=live.get("city", city),
            weather=live.get("weather", ""),
            temperature=live.get("temperature", "") + "°C",
            humidity=live.get("humidity", "") + "%",
            wind=f"{live.get('winddirection', '')}风{live.get('windpower', '')}级",
            report_time=live.get("reporttime", "")
        )
        
        print(f"   ✅ 天气: {result.weather}, 温度: {result.temperature}")
        return result


# ===== Concierge Agent（礼宾员 - 酒店餐厅）=====

class ConciergeAgent(BaseAgent):
    """
    礼宾员Agent - 负责酒店和餐厅推荐
    
    🧒 小学生讲解:
    礼宾员就像酒店前台的服务员，帮你安排住宿和吃饭。
    "您想住五星酒店还是经济型？""晚上想吃什么菜系？"
    """
    
    AMAP_POI_SEARCH_URL = "https://restapi.amap.com/v3/place/text"
    
    # 模拟数据
    MOCK_HOTELS = {
        "北京": [
            HotelResult(name="北京饭店", address="东城区东长安街33号", 
                       location="116.415856,39.912345", rating=4.7, price_range="¥800-1500"),
            HotelResult(name="如家快捷酒店", address="朝阳区建国路", 
                       location="116.468123,39.910234", rating=4.2, price_range="¥200-350"),
        ]
    }
    
    async def search_hotels(
        self, 
        city: str, 
        budget_level: str = "中等",
        limit: int = 5
    ) -> List[HotelResult]:
        """
        搜索酒店
        
        Args:
            city: 城市名称
            budget_level: 预算级别（低/中等/高）
            limit: 返回数量
        """
        print(f"🏨 Concierge: 在{city}搜索{budget_level}预算酒店...")
        
        # 映射预算到关键词
        budget_keywords = {
            "低": "经济型酒店",
            "中等": "商务酒店",
            "高": "五星级酒店"
        }
        keyword = budget_keywords.get(budget_level, "酒店")
        
        if not self.amap_key:
            mock_results = self.MOCK_HOTELS.get(city, [])[:limit]
            print(f"   📦 返回{len(mock_results)}个模拟结果")
            return mock_results
        
        # 调用API...（与Scout类似，略）
        return []
    
    async def search_restaurants(
        self, 
        city: str, 
        cuisine: str = "美食",
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        搜索餐厅
        
        Args:
            city: 城市名称
            cuisine: 菜系类型
            limit: 返回数量
        """
        print(f"🍽️ Concierge: 在{city}搜索{cuisine}...")
        
        # 简化实现，返回模拟数据
        return [
            {"name": f"{city}特色餐厅1", "cuisine": cuisine, "rating": 4.5},
            {"name": f"{city}特色餐厅2", "cuisine": cuisine, "rating": 4.3},
        ]


# ===== MCP服务器封装（进阶） =====
# 使用FastMCP将Agent能力暴露为标准MCP工具

def create_mcp_server():
    """
    创建MCP服务器，将所有Agent能力注册为工具
    
    🧒 小学生讲解:
    MCP服务器就像一个"工具柜台"，Agent可以来这里"借工具"。
    我们把Scout、Meteorologist、Concierge的能力都放到柜台上。
    """
    try:
        from fastmcp import FastMCP
    except ImportError:
        print("请先安装 fastmcp: pip install fastmcp")
        return None
    
    mcp = FastMCP("TravelAgents工具箱")
    
    # 初始化各Agent
    scout = ScoutAgent()
    meteorologist = MeteorologistAgent()
    concierge = ConciergeAgent()
    
    # 注册工具
    @mcp.tool()
    async def search_attractions(city: str, keyword: str = "景点", limit: int = 5):
        """
        搜索城市景点。返回景点名称、地址、坐标和评分。
        
        Args:
            city: 城市名称，如"北京"
            keyword: 搜索关键词，如"博物馆"、"公园"
            limit: 返回结果数量
        """
        results = await scout.search_attractions(city, keyword, limit)
        return [r.model_dump() for r in results]
    
    @mcp.tool()
    async def get_weather(city: str):
        """
        获取城市当前天气。返回温度、天气状况、湿度和风力。
        
        Args:
            city: 城市名称
        """
        result = await meteorologist.get_weather(city)
        return result.model_dump()
    
    @mcp.tool()
    async def search_hotels(city: str, budget: str = "中等", limit: int = 5):
        """
        搜索酒店。根据预算级别推荐合适的酒店。
        
        Args:
            city: 城市名称
            budget: 预算级别（低/中等/高）
            limit: 返回数量
        """
        results = await concierge.search_hotels(city, budget, limit)
        return [r.model_dump() for r in results]
    
    return mcp


# ===== 测试代码 =====

async def main():
    """测试所有Agent"""
    print("=" * 60)
    print("🔧 Phase 3: 专家Agents测试")
    print("=" * 60)
    
    # 测试Scout
    print("\n--- 🔭 Scout Agent (侦察兵) ---")
    scout = ScoutAgent()
    attractions = await scout.search_attractions("北京", "历史文化")
    for a in attractions:
        print(f"  • {a.name} | 评分: {a.rating} | {a.address[:20]}...")
    
    # 测试Meteorologist
    print("\n--- 🌤️ Meteorologist Agent (气象员) ---")
    meteo = MeteorologistAgent()
    weather = await meteo.get_weather("北京")
    print(f"  {weather.city}: {weather.weather}, {weather.temperature}")
    
    # 测试Concierge
    print("\n--- 🏨 Concierge Agent (礼宾员) ---")
    concierge = ConciergeAgent()
    hotels = await concierge.search_hotels("北京", "中等")
    for h in hotels:
        print(f"  • {h.name} | {h.price_range}")
    
    print("\n✅ 所有Agent测试完成!")


async def test_specialists():
    """验收测试"""
    print("\n📋 开始专家Agent验收测试...\n")
    
    tests_passed = 0
    
    # 测试1: Scout能返回景点
    scout = ScoutAgent()
    attractions = await scout.search_attractions("北京")
    if len(attractions) > 0:
        print("✅ Scout: 成功返回景点数据")
        tests_passed += 1
    else:
        print("❌ Scout: 未返回数据")
    
    # 测试2: Meteorologist能返回天气
    meteo = MeteorologistAgent()
    weather = await meteo.get_weather("上海")
    if weather.weather != "未知":
        print("✅ Meteorologist: 成功返回天气数据")
        tests_passed += 1
    else:
        print("❌ Meteorologist: 未返回数据")
    
    # 测试3: Concierge能返回酒店
    concierge = ConciergeAgent()
    hotels = await concierge.search_hotels("北京")
    if len(hotels) > 0:
        print("✅ Concierge: 成功返回酒店数据")
        tests_passed += 1
    else:
        print("❌ Concierge: 未返回数据")
    
    print(f"\n📊 测试结果: {tests_passed}/3 通过")


if __name__ == "__main__":
    import asyncio
    import sys
    
    if "--test" in sys.argv:
        asyncio.run(test_specialists())
    elif "--mcp" in sys.argv:
        # 启动MCP服务器
        mcp = create_mcp_server()
        if mcp:
            mcp.run()
    else:
        asyncio.run(main())
