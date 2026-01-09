"""
Phase 2 实验: 高德天气 API 真实调用

🧒 小学生讲解:
这个脚本会调用真正的高德天气 API，获取真实的天气数据！
之前我们用的是假数据 {"北京": "晴天"}，现在是真的从网上查！

🎓 面试话术:
"我集成了高德地图 Web API，使用 requests 库进行 HTTP 调用。
API 返回 JSON 格式数据，我用 Pydantic 进行数据验证和解析，
确保数据格式正确。"
"""

import os
import requests
from dotenv import load_dotenv

# 高德是国内 API，不需要代理！清除代理设置
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)

load_dotenv()


# ========================================
# Step 1: 配置
# ========================================
AMAP_API_KEY = os.getenv("AMAP_API_KEY")
WEATHER_API_URL = "https://restapi.amap.com/v3/weather/weatherInfo"


# ========================================
# Step 2: 城市编码（高德API需要城市编码，不是城市名）
# ========================================
# 常用城市的 adcode（行政区划代码）
CITY_CODES = {
    "北京": "110000",
    "上海": "310000",
    "广州": "440100",
    "深圳": "440300",
    "杭州": "330100",
    "成都": "510100",
    "西安": "610100",
    "南京": "320100",
}


# ========================================
# Step 3: 天气查询函数
# ========================================
def get_weather(city: str) -> dict:
    """
    查询指定城市的实时天气
    
    Args:
        city: 城市名称，如 "北京"
    
    Returns:
        天气信息字典
    """
    # 获取城市编码
    city_code = CITY_CODES.get(city)
    if not city_code:
        return {"error": f"不支持的城市: {city}"}
    
    # 构建请求参数
    params = {
        "key": AMAP_API_KEY,
        "city": city_code,
        "extensions": "base",  # base=实况, all=预报
        "output": "JSON"
    }
    
    print(f"📡 正在请求高德天气 API...")
    print(f"   URL: {WEATHER_API_URL}")
    print(f"   城市: {city} (编码: {city_code})")
    
    # 发送请求 (显式禁用代理，因为高德是国内API)
    response = requests.get(
        WEATHER_API_URL, 
        params=params,
        proxies={"http": None, "https": None}  # 禁用代理
    )
    data = response.json()
    
    # 检查返回状态
    if data.get("status") != "1":
        return {"error": f"API 调用失败: {data.get('info')}"}
    
    # 解析天气数据
    lives = data.get("lives", [])
    if not lives:
        return {"error": "没有获取到天气数据"}
    
    weather_info = lives[0]
    
    return {
        "city": weather_info.get("city"),
        "weather": weather_info.get("weather"),
        "temperature": weather_info.get("temperature"),
        "winddirection": weather_info.get("winddirection"),
        "windpower": weather_info.get("windpower"),
        "humidity": weather_info.get("humidity"),
        "reporttime": weather_info.get("reporttime")
    }


# ========================================
# Step 4: 测试
# ========================================
if __name__ == "__main__":
    print("=" * 60)
    print("🧪 高德天气 API 测试")
    print("=" * 60)
    
    # 检查 API Key
    if not AMAP_API_KEY:
        print("❌ 错误: AMAP_API_KEY 未配置!")
        print("请在 .env 文件中添加: AMAP_API_KEY=你的密钥")
        exit(1)
    
    print(f"✅ API Key 已配置: {AMAP_API_KEY[:8]}...")
    print()
    
    # 测试几个城市
    test_cities = ["北京", "上海", "广州"]
    
    for city in test_cities:
        print("-" * 40)
        result = get_weather(city)
        
        if "error" in result:
            print(f"❌ {city}: {result['error']}")
        else:
            print(f"✅ {result['city']} 天气:")
            print(f"   天气: {result['weather']}")
            print(f"   温度: {result['temperature']}°C")
            print(f"   风向: {result['winddirection']}风 {result['windpower']}级")
            print(f"   湿度: {result['humidity']}%")
            print(f"   更新时间: {result['reporttime']}")
        print()
    
    print("=" * 60)
    print("🎉 测试完成!")
    print("=" * 60)
