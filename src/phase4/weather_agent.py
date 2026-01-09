"""
Phase 4.2: Meteorologist Agent (气象员) 🌤️
专注于天气查询的 MCP 服务。
强调：错误处理、参数校验。
"""

import os
import requests
from dotenv import load_dotenv
from fastmcp import FastMCP
from typing import Optional

# 1. 初始化 Server
mcp = FastMCP("Meteorologist Agent")

# 加载环境变量
load_dotenv()
AMAP_API_KEY = os.getenv("AMAP_API_KEY")

# 城市编码映射 (模拟数据库)
CITY_CODES = {
    "北京": "110000",
    "上海": "310000",
    "广州": "440100",
    "深圳": "440300",
    "杭州": "330100",
    "南京": "320100"
}

# 2. 核心逻辑 (分离)
def _get_weather_logic(city: str) -> str:
    # 2.1 参数校验 (Validation)
    if not city:
        return "❌ 错误: 城市名称不能为空"
    
    # 清洗输入 (简单处理)
    clean_city = city.strip().replace("市", "")
    
    city_code = CITY_CODES.get(clean_city)
    if not city_code:
        # 友好报错 (Robustness)
        supported = ", ".join(CITY_CODES.keys())
        return f"⚠️ 抱歉，我目前不支持查询 '{city}' 的天气。\n✅ 支持的城市: {supported}"

    if not AMAP_API_KEY:
        return "❌ 错误: 服务端未配置 AMAP_API_KEY"

    # 2.2 API 调用
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    try:
        resp = requests.get(
            url, 
            params={"key": AMAP_API_KEY, "city": city_code, "extensions": "base"},
            proxies={"http": None, "https": None}, # 关键: 禁用代理
            timeout=5
        )
        resp.raise_for_status() # 检查 HTTP 错误
        
        data = resp.json()
        if data["status"] == "1" and data["lives"]:
            live = data["lives"][0]
            # 2.3 格式化输出
            return (
                f"🌤️ {clean_city}天气实况:\n"
                f"- 天气: {live['weather']}\n"
                f"- 温度: {live['temperature']}℃\n"
                f"- 湿度: {live['humidity']}%\n"
                f"- 风向: {live['winddirection']}风 {live['windpower']}级\n"
                f"(更新时间: {live['reporttime']})"
            )
        else:
            return f"API 返回错误: {data.get('info', '未知错误')}"
            
    except requests.Timeout:
        return "❌ 错误: 请求超时，请稍后再试"
    except Exception as e:
        return f"❌ 系统异常: {str(e)}"

# 3. 注册工具
@mcp.tool(description="查询中国主要城市的实时天气情况")
def get_weather(city: str) -> str:
    """
    获取天气信息
    
    Args:
        city: 城市中文名称 (如 "北京", "上海")
    """
    return _get_weather_logic(city)

if __name__ == "__main__":
    mcp.run()
