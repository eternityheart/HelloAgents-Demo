"""
Phase 8.1: Hotel Agent (酒店推荐员) 🏨
使用 FastMCP 将酒店搜索功能封装为独立服务。

功能:
- 提供 search_hotel 工具
- 支持评分筛选
- 基于高德 API
"""

import os
import requests
from dotenv import load_dotenv
from fastmcp import FastMCP

# 1. 初始化 MCP 服务器
mcp = FastMCP("Hotel Agent")

# 加载环境变量
load_dotenv()
AMAP_API_KEY = os.getenv("AMAP_API_KEY")

# 酒店类型代码
HOTEL_TYPES = {
    "酒店": "100000",       # 一级分类
    "星级酒店": "100100",   # 五星/四星
    "经济型酒店": "100200",
    "公寓式酒店": "100300",
    "民宿": "100400"
}

# 2. 核心逻辑
def _search_hotel_logic(
    city: str, 
    keyword: str = "酒店",
    hotel_type: str = "酒店",
    min_rating: float = 0.0,
    max_results: int = 5
) -> str:
    """搜索酒店的核心逻辑"""
    if not AMAP_API_KEY:
        return "❌ 错误: AMAP_API_KEY 未配置"
    
    url = "https://restapi.amap.com/v3/place/text"
    type_code = HOTEL_TYPES.get(hotel_type, "100000")
    
    try:
        resp = requests.get(
            url,
            params={
                "key": AMAP_API_KEY,
                "city": city,
                "keywords": keyword,
                "types": type_code,
                "citylimit": "true",
                "offset": max_results * 3  # 多请求一些用于过滤
            },
            proxies={"http": None, "https": None},
            timeout=5
        )
        data = resp.json()
        
        if data["status"] != "1":
            return f"API错误: {data.get('info')}"
        
        pois = data.get("pois", [])
        if not pois:
            return f"在{city}未找到'{keyword}'相关酒店"
        
        # 过滤和格式化结果
        results = []
        for poi in pois:
            # 获取评分
            biz_ext = poi.get("biz_ext", {})
            rating_str = biz_ext.get("rating", "0")
            try:
                rating = float(rating_str) if rating_str else 0.0
            except:
                rating = 0.0
            
            # 评分过滤
            if rating < min_rating:
                continue
            
            name = poi.get("name", "未知")
            address = poi.get("address", "地址未知")
            tel = poi.get("tel", "")
            location = poi.get("location", "")
            
            results.append({
                "name": name,
                "rating": rating,
                "address": address,
                "tel": tel,
                "location": location
            })
            
            if len(results) >= max_results:
                break
        
        if not results:
            return f"在{city}未找到评分高于 {min_rating} 的酒店"
        
        # 格式化输出
        output_lines = []
        for i, hotel in enumerate(results, 1):
            rating_display = f"{hotel['rating']:.1f}" if hotel['rating'] > 0 else "暂无"
            output_lines.append(
                f"{i}. {hotel['name']} (评分:{rating_display}) - {hotel['address']}"
            )
        
        return "\n".join(output_lines)
        
    except Exception as e:
        return f"连接异常: {str(e)}"

# 3. 定义 MCP 工具
@mcp.tool(description="搜索酒店，支持评分筛选")
def search_hotel(
    city: str,
    keyword: str = "酒店",
    hotel_type: str = "酒店", 
    min_rating: float = 0.0,
    max_results: int = 5
) -> str:
    """
    搜索酒店信息
    
    Args:
        city: 城市名称 (如 "北京")
        keyword: 搜索关键词 (如 "五星级" 或具体酒店名)
        hotel_type: 酒店类型 ("酒店", "星级酒店", "经济型酒店", "公寓式酒店", "民宿")
        min_rating: 最低评分要求 (0-5, 默认0不过滤)
        max_results: 返回结果数量 (默认5)
    
    Returns:
        格式化的酒店列表
    """
    return _search_hotel_logic(city, keyword, hotel_type, min_rating, max_results)

# 4. 直接调用函数 (供 Orchestrator 直接使用)
def get_hotels(city: str, keyword: str = "酒店", min_rating: float = 4.0) -> str:
    """供其他模块直接调用的简化接口"""
    return _search_hotel_logic(city, keyword, "酒店", min_rating, 5)

# 5. 入口点
if __name__ == "__main__":
    # 测试模式
    print("🏨 Hotel Agent 测试")
    print("-" * 40)
    result = search_hotel("北京", "五星级酒店", min_rating=4.0)
    print(result)
    print("-" * 40)
    # MCP 服务模式
    # mcp.run()
