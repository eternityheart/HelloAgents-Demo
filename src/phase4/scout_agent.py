"""
Phase 4.1: Scout Agent (侦察兵) 🔭
使用 FastMCP 将 POI 搜索功能封装为独立服务。

功能:
- 提供 search_poi 工具
- 基于高德 API
- 独立进程运行
"""

import os
import requests
from dotenv import load_dotenv
from fastmcp import FastMCP

# 1. 初始化 MCP 服务器
# name: 服务名称
# dependencies: 自动安装依赖 (可选，这里我们手动管理)
mcp = FastMCP("Scout Agent")

# 加载环境变量
load_dotenv()
AMAP_API_KEY = os.getenv("AMAP_API_KEY")

# 常量定义
POI_TYPES = {
    "景点": "110000",
    "餐厅": "050000",
    "酒店": "100000"
}

# 2. 核心逻辑 (分离以便测试)
def _search_poi_logic(city: str, keyword: str, poi_type: str = "景点") -> str:
    if not AMAP_API_KEY:
        return "❌ 错误: AMAP_API_KEY 未配置"
        
    url = "https://restapi.amap.com/v3/place/text"
    type_code = POI_TYPES.get(poi_type, "110000")
    
    try:
        # 高德 API 调用 (显式禁用代理)
        resp = requests.get(
            url,
            params={
                "key": AMAP_API_KEY,
                "city": city,
                "keywords": keyword,
                "types": type_code,
                "citylimit": "true",
                "offset": 5
            },
            proxies={"http": None, "https": None},
            timeout=5
        )
        data = resp.json()
        
        if data["status"] == "1":
            pois = data.get("pois", [])
            if not pois:
                return f"在{city}未找到名为'{keyword}'的{poi_type}"
                
            results = []
            for i, poi in enumerate(pois, 1):
                name = poi.get("name")
                addr = poi.get("address")
                rating = poi.get("biz_ext", {}).get("rating", "无")
                results.append(f"{i}. {name} (评分:{rating}) - {addr}")
            
            return "\n".join(results)
            
        return f"API错误: {data.get('info')}"
        
    except Exception as e:
        return f"连接异常: {str(e)}"

# 3. 定义工具 (使用装饰器)
@mcp.tool(description="搜索指定城市的兴趣点(POI)，如景点、餐厅、酒店")
def search_poi(city: str, keyword: str, poi_type: str = "景点") -> str:
    """
    搜索地点信息
    
    Args:
        city: 城市名称 (如 "北京")
        keyword: 搜索关键词 (如 "故宫")
        poi_type: 类型筛选 ("景点", "餐厅", "酒店")
    """
    return _search_poi_logic(city, keyword, poi_type)

# 3. 入口点
if __name__ == "__main__":
    # 默认 run() 会启动 stdio 服务
    mcp.run()
