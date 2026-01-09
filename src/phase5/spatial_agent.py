"""
Phase 5.3: Spatial Agent (空间感知侦察兵) 🧠
继承自 Scout Agent，但增加了空间感知能力。
"""

import os
import requests
from dotenv import load_dotenv
from fastmcp import FastMCP
from data_processor import process_pois

# 初始化
mcp = FastMCP("Spatial Scout")
load_dotenv()
AMAP_API_KEY = os.getenv("AMAP_API_KEY")

POI_TYPES = {
    "景点": "110000",
    "餐厅": "050000",
    "酒店": "100000",
    "加油站": "010100",
    "厕所": "200300"
}

# 逻辑分离
def _search_nearby_logic(keyword: str, user_lat: float, user_lon: float, city: str = "北京", poi_type: str = "景点") -> str:
    if not AMAP_API_KEY:
        return "❌ 错误: AMAP_API_KEY 未配置"
        
    url = "https://restapi.amap.com/v3/place/text"
    type_code = POI_TYPES.get(poi_type, "110000")
    
    try:
        resp = requests.get(
            url,
            params={
                "key": AMAP_API_KEY,
                "city": city,
                "keywords": keyword,
                "types": type_code,
                "citylimit": "true",
                "offset": 10
            },
            proxies={"http": None, "https": None},
            timeout=5
        )
        data = resp.json()
        
        if data["status"] == "1":
            raw_pois = data.get("pois", [])
            return process_pois(raw_pois, user_lat, user_lon)
            
        return f"API错误: {data.get('info')}"
        
    except Exception as e:
        return f"连接异常: {str(e)}"

@mcp.tool(description="搜索附近的地点，并按距离排序")
def search_nearby(keyword: str, user_lat: float, user_lon: float, city: str = "北京", poi_type: str = "景点") -> str:
    """
    搜索周边 POI
    
    Args:
        keyword: 关键词 (如 "必胜客")
        user_lat: 用户纬度
        user_lon: 用户经度
        city: 城市名称
        poi_type: 类型
    """
    return _search_nearby_logic(keyword, user_lat, user_lon, city, poi_type)

if __name__ == "__main__":
    mcp.run()
