"""
Day 2.2 实验: 高德 POI 搜索 API

🧒 小学生讲解:
POI = Point of Interest = 兴趣点
可以搜索景点、餐厅、酒店、加油站等任何"地点"！
这样 Scout Worker 就能查真实的景点推荐了。

🎓 面试话术:
"我集成了高德 POI 搜索 API，支持关键词搜索和分类搜索。
通过 types 参数可以筛选类型（景点、餐厅等），
通过 city 参数限定城市范围，提高搜索精度。"
"""

import os
import requests
from dotenv import load_dotenv

# 高德是国内 API，不需要代理
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)

load_dotenv()


# ========================================
# Step 1: 配置
# ========================================
AMAP_API_KEY = os.getenv("AMAP_API_KEY")
POI_SEARCH_URL = "https://restapi.amap.com/v3/place/text"

# POI 类型代码（高德官方定义）
# 完整列表：https://lbs.amap.com/api/webservice/download
POI_TYPES = {
    "景点": "110000",      # 风景名胜
    "餐厅": "050000",      # 餐饮服务
    "酒店": "100000",      # 住宿服务
    "购物": "060000",      # 购物服务
    "交通": "150000",      # 交通设施
}


# ========================================
# Step 2: POI 搜索函数
# ========================================
def search_poi(city: str, keyword: str = None, poi_type: str = None, limit: int = 5) -> list:
    """
    搜索指定城市的兴趣点
    
    Args:
        city: 城市名称
        keyword: 搜索关键词（如"故宫"）
        poi_type: POI类型（景点/餐厅/酒店）
        limit: 返回结果数量
    
    Returns:
        POI 列表
    """
    # 构建请求参数
    params = {
        "key": AMAP_API_KEY,
        "city": city,
        "citylimit": "true",  # 限制在指定城市内搜索
        "offset": limit,
        "output": "JSON"
    }
    
    # 添加关键词或类型
    if keyword:
        params["keywords"] = keyword
    if poi_type and poi_type in POI_TYPES:
        params["types"] = POI_TYPES[poi_type]
    
    print(f"📡 正在搜索 {city} 的 {poi_type or ''}POI...")
    if keyword:
        print(f"   关键词: {keyword}")
    
    # 发送请求
    response = requests.get(
        POI_SEARCH_URL,
        params=params,
        proxies={"http": None, "https": None}
    )
    data = response.json()
    
    # 检查返回状态
    if data.get("status") != "1":
        print(f"❌ 错误: {data.get('info')}")
        return []
    
    # 解析结果
    pois = data.get("pois", [])
    results = []
    
    for poi in pois:
        results.append({
            "name": poi.get("name"),
            "type": poi.get("type"),
            "address": poi.get("address"),
            "tel": poi.get("tel", "暂无"),
            "rating": poi.get("biz_ext", {}).get("rating", "暂无评分")
        })
    
    return results


# ========================================
# Step 3: 测试
# ========================================
if __name__ == "__main__":
    print("=" * 60)
    print("🧪 高德 POI 搜索 API 测试")
    print("=" * 60)
    
    # 检查 API Key
    if not AMAP_API_KEY:
        print("❌ 错误: AMAP_API_KEY 未配置!")
        exit(1)
    
    print(f"✅ API Key 已配置: {AMAP_API_KEY[:8]}...")
    print()
    
    # 测试 1: 搜索北京的景点
    print("-" * 40)
    print("测试 1: 搜索北京的景点")
    print("-" * 40)
    results = search_poi("北京", poi_type="景点", limit=5)
    for i, r in enumerate(results, 1):
        print(f"  {i}. {r['name']}")
        print(f"     类型: {r['type']}")
        print(f"     地址: {r['address']}")
    print()
    
    # 测试 2: 关键词搜索
    print("-" * 40)
    print("测试 2: 关键词搜索 '故宫'")
    print("-" * 40)
    results = search_poi("北京", keyword="故宫", limit=3)
    for i, r in enumerate(results, 1):
        print(f"  {i}. {r['name']}")
        print(f"     地址: {r['address']}")
    print()
    
    # 测试 3: 搜索上海的餐厅
    print("-" * 40)
    print("测试 3: 搜索上海的餐厅")
    print("-" * 40)
    results = search_poi("上海", poi_type="餐厅", limit=5)
    for i, r in enumerate(results, 1):
        print(f"  {i}. {r['name']}")
        print(f"     地址: {r['address']}")
    print()
    
    print("=" * 60)
    print("🎉 测试完成!")
    print("=" * 60)
