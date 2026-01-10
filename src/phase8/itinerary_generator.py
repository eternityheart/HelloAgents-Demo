"""
Phase 8.2: 多日行程生成器 (Itinerary Generator) ⭐
核心功能: 整合多Agent结果，生成结构化的多日旅行方案
"""

import sys
import os
from typing import List
from datetime import datetime, timedelta

# 确保能导入项目模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phase8.models import POI, DayPlan, Itinerary
from phase3.tools import get_weather, search_poi
from phase4.hotel_agent import _search_hotel_logic


class ItineraryGenerator:
    """多日行程生成器"""
    
    def __init__(self):
        self.weather_cache = {}
        self.attractions_pool = []
        self.restaurants_pool = []
        self.hotels_pool = []
    
    def generate(self, city: str, days: int, preferences: List[str] = None, start_date: str = None) -> Itinerary:
        """
        生成多日行程
        
        Args:
            city: 目的地城市
            days: 行程天数 (1-7)
            preferences: 用户偏好标签 (如 ["历史", "美食"])
            start_date: 出发日期 (YYYY-MM-DD格式，默认明天)
        
        Returns:
            Itinerary: 结构化行程对象
        """
        preferences = preferences or []
        
        # 1. 计算日期
        if start_date:
            base_date = datetime.strptime(start_date, "%Y-%m-%d")
        else:
            base_date = datetime.now() + timedelta(days=1)
        
        # 2. 获取天气
        weather_info = self._get_weather(city)
        
        # 3. 搜索景点 (根据偏好)
        self._search_attractions(city, preferences)
        
        # 4. 搜索餐厅
        self._search_restaurants(city)
        
        # 5. 搜索酒店
        self._search_hotels(city)
        
        # 6. 组装每日行程
        day_plans = []
        for d in range(1, days + 1):
            current_date = base_date + timedelta(days=d-1)
            
            plan = DayPlan(
                day=d,
                date=current_date.strftime("%Y-%m-%d"),
                weather=weather_info,
                weather_tip=self._get_weather_tip(weather_info),
                morning=self._pick_attractions(2),
                afternoon=self._pick_attractions(1),
                dinner=self._pick_restaurant(),
                hotel=self._pick_hotel() if d < days else None  # 最后一天不需要酒店
            )
            day_plans.append(plan)
        
        # 7. 生成行程概述
        summary = self._generate_summary(city, days, preferences)
        
        return Itinerary(
            city=city,
            days=days,
            preferences=preferences,
            summary=summary,
            itinerary=day_plans,
            tips=self._generate_tips(city, weather_info)
        )
    
    def _get_weather(self, city: str) -> str:
        """获取天气信息"""
        if city in self.weather_cache:
            return self.weather_cache[city]
        
        try:
            result = get_weather(city)
            self.weather_cache[city] = result
            return result
        except Exception as e:
            return f"天气获取失败: {e}"
    
    def _get_weather_tip(self, weather: str) -> str:
        """根据天气生成提示"""
        if "雨" in weather:
            return "🌧️ 建议携带雨具，优先安排室内活动"
        elif "晴" in weather:
            return "☀️ 天气晴好，适合户外游览"
        elif "阴" in weather or "多云" in weather:
            return "☁️ 阴天凉爽，适合各类活动"
        elif "雪" in weather:
            return "❄️ 注意保暖，可欣赏雪景"
        else:
            return "请关注天气变化"
    
    def _search_attractions(self, city: str, preferences: List[str]):
        """搜索景点"""
        keywords = preferences[:2] if preferences else ["景点", "必去"]
        
        for keyword in keywords:
            try:
                result = search_poi(city, keyword, "景点")
                self._parse_and_add_pois(result, self.attractions_pool, "景点")
            except Exception as e:
                print(f"景点搜索失败: {e}")
    
    def _search_restaurants(self, city: str):
        """搜索餐厅"""
        try:
            result = search_poi(city, "美食", "餐厅")
            self._parse_and_add_pois(result, self.restaurants_pool, "餐厅")
        except Exception as e:
            print(f"餐厅搜索失败: {e}")
    
    def _search_hotels(self, city: str):
        """搜索酒店"""
        try:
            result = _search_hotel_logic(city, "酒店", "酒店", 4.0, 5)
            self._parse_and_add_pois(result, self.hotels_pool, "酒店")
        except Exception as e:
            print(f"酒店搜索失败: {e}")
    
    def _parse_and_add_pois(self, result: str, pool: List[POI], poi_type: str):
        """解析 POI 搜索结果并添加到池中"""
        if not result or "错误" in result or "未找到" in result:
            return
        
        for line in result.split("\n"):
            if not line.strip():
                continue
            try:
                # 解析格式: "1. 名称 (评分:X.X) - 地址"
                parts = line.split(".", 1)
                if len(parts) < 2:
                    continue
                
                rest = parts[1].strip()
                
                # 提取名称
                if "(" in rest:
                    name = rest.split("(")[0].strip()
                else:
                    name = rest.split("-")[0].strip()
                
                # 提取评分
                rating = None
                if "评分:" in rest:
                    rating_str = rest.split("评分:")[1].split(")")[0]
                    try:
                        rating = float(rating_str)
                    except:
                        pass
                
                # 提取地址
                address = None
                if "-" in rest:
                    address = rest.split("-", 1)[1].strip()
                
                poi = POI(
                    name=name,
                    rating=rating,
                    address=address,
                    type=poi_type
                )
                pool.append(poi)
                
            except Exception as e:
                continue
    
    def _pick_attractions(self, count: int) -> List[POI]:
        """从景点池中选取"""
        picked = []
        for _ in range(count):
            if self.attractions_pool:
                picked.append(self.attractions_pool.pop(0))
        return picked
    
    def _pick_restaurant(self) -> POI:
        """从餐厅池中选取一个"""
        if self.restaurants_pool:
            return self.restaurants_pool.pop(0)
        return None
    
    def _pick_hotel(self) -> POI:
        """从酒店池中选取一个"""
        if self.hotels_pool:
            return self.hotels_pool.pop(0)
        return None
    
    def _generate_summary(self, city: str, days: int, preferences: List[str]) -> str:
        """生成行程概述"""
        pref_text = "、".join(preferences) if preferences else "休闲"
        return f"这是一份精心规划的{city}{days}日游方案，以{pref_text}为主题，带您深度体验这座城市的魅力。"
    
    def _generate_tips(self, city: str, weather: str) -> List[str]:
        """生成旅行贴士"""
        tips = [
            f"📱 建议下载高德地图导航",
            f"💳 大部分地方支持移动支付",
            f"🎫 热门景点建议提前网上预约"
        ]
        
        if "雨" in weather:
            tips.append("☔ 携带雨具")
        if "冷" in weather or "低温" in weather:
            tips.append("🧥 注意保暖")
            
        return tips


# 便捷函数
def generate_itinerary(city: str, days: int, preferences: List[str] = None) -> Itinerary:
    """便捷函数: 生成行程"""
    gen = ItineraryGenerator()
    return gen.generate(city, days, preferences)


# 测试
if __name__ == "__main__":
    print("=" * 60)
    print("🗺️ 多日行程生成器测试")
    print("=" * 60)
    
    result = generate_itinerary("北京", 3, ["历史", "美食"])
    
    print(f"\n📍 目的地: {result.city}")
    print(f"📅 天数: {result.days}")
    print(f"📝 概述: {result.summary}")
    print()
    
    for day in result.itinerary:
        print(f"--- 第 {day.day} 天 ({day.date}) ---")
        print(f"🌤️ 天气: {day.weather}")
        print(f"💡 提示: {day.weather_tip}")
        print(f"🌅 上午: {', '.join([p.name for p in day.morning]) if day.morning else '自由活动'}")
        print(f"🌇 下午: {', '.join([p.name for p in day.afternoon]) if day.afternoon else '自由活动'}")
        print(f"🍽️ 晚餐: {day.dinner.name if day.dinner else '自选'}")
        print(f"🏨 住宿: {day.hotel.name if day.hotel else '无'}")
        print()
    
    print("📌 旅行贴士:")
    for tip in result.tips or []:
        print(f"  • {tip}")
    
    print("\n✅ 测试完成!")
