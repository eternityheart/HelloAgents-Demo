"""
Phase 3 Tools: 封装高德 API
将 Phase 2 的实验代码封装为生产级函数。
"""

import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
AMAP_API_KEY = os.getenv("AMAP_API_KEY")

# 城市编码映射
CITY_CODES = {
    "北京": "110000",
    "上海": "310000",
    "广州": "440100",
    "深圳": "440300"
}

# POI 类型映射
POI_TYPES = {
    "景点": "110000",
    "餐厅": "050000",
    "酒店": "100000"
}

def get_weather(city: str) -> str:
    """
    查询指定城市的实时天气
    """
    if not AMAP_API_KEY:
        return "❌ 配置错误: AMAP_API_KEY 未找到"

    city_code = CITY_CODES.get(city)
    if not city_code:
        return f"⚠️ 暂不支持城市: {city} (仅支持: {', '.join(CITY_CODES.keys())})"
    
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    try:
        # 显式禁用代理
        resp = requests.get(
            url, 
            params={"key": AMAP_API_KEY, "city": city_code, "extensions": "base"},
            proxies={"http": None, "https": None},
            timeout=5
        )
        data = resp.json()
        
        if data["status"] == "1" and data["lives"]:
            live = data["lives"][0]
            # 返回自然语言描述，方便 Agent 理解
            return (
                f"{city}天气实况:\n"
                f"- 天气: {live['weather']}\n"
                f"- 温度: {live['temperature']}℃\n"
                f"- 风力: {live['winddirection']}风 {live['windpower']}级\n"
                f"- 湿度: {live['humidity']}%"
            )
        return f"查询失败: {data.get('info', '未知错误')}"
        
    except Exception as e:
        return f"API调用异常: {str(e)}"

def search_poi(city: str, keyword: str, poi_type: str = "景点") -> str:
    """
    搜索指定城市的地点信息
    """
    if not AMAP_API_KEY:
        return "❌ 配置错误: AMAP_API_KEY 未找到"

    type_code = POI_TYPES.get(poi_type, "110000")
    url = "https://restapi.amap.com/v3/place/text"
    
    try:
        # 显式禁用代理
        resp = requests.get(
            url,
            params={
                "key": AMAP_API_KEY,
                "city": city,
                "keywords": keyword,
                "types": type_code,
                "citylimit": "true",
                "offset": 5  # 限制5条
            },
            proxies={"http": None, "https": None},
            timeout=5
        )
        data = resp.json()
        
        if data["status"] == "1":
            pois = data.get("pois", [])
            if not pois:
                return f"在{city}未找到名为'{keyword}'的{poi_type}"
            
            result_lines = [f"在{city}找到以下'{keyword}'({poi_type}):"]
            for i, poi in enumerate(pois, 1):
                name = poi.get("name")
                address = poi.get("address")
                rating = poi.get("biz_ext", {}).get("rating", "无评分")
                result_lines.append(f"{i}. {name} (评分: {rating})\n   地址: {address}")
            
            return "\n".join(result_lines)
            
        return f"查询失败: {data.get('info', '未知错误')}"
        
    except Exception as e:
        return f"API调用异常: {str(e)}"
