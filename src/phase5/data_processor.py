"""
Phase 5.2: Data Processor 🧹
负责处理原始 API 数据，增加空间维度。

核心功能:
1. 距离计算: 对每个 POI 计算到用户的距离
2. 排序: 按距离由近到远排序
3. 格式化: 输出带距离信息的友好文本
"""

from typing import List, Dict, Any, Tuple
from geo_utils import haversine_distance, parse_location

def process_pois(pois: List[Dict[str, Any]], user_lat: float, user_lon: float) -> str:
    """
    处理 POI 列表: 计算距离并排序
    
    Args:
        pois: 高德 API 返回的原始 POI 字典列表
        user_lat, user_lon: 用户当前位置
        
    Returns:
        str: 格式化后的文本列表
    """
    if not pois:
        return "未找到相关地点。"

    # 1. 增强数据 (Enrichment)
    # 为每个 POI 加上 _distance 字段
    enriched_pois = []
    for poi in pois:
        loc_str = poi.get("location", "")
        poi_lat, poi_lon = parse_location(loc_str)
        
        # 如果坐标无效，距离设为无穷大，放到最后
        if poi_lat == 0 and poi_lon == 0:
            dist = float('inf')
        else:
            dist = haversine_distance(user_lat, user_lon, poi_lat, poi_lon)
            
        poi["_distance"] = dist
        enriched_pois.append(poi)

    # 2. 排序 (Sorting)
    # 按 _distance 从小到大排
    enriched_pois.sort(key=lambda x: x["_distance"])

    # 3. 格式化输出 (Formatting)
    result_lines = []
    for i, poi in enumerate(enriched_pois, 1):
        name = poi.get("name", "未知地点")
        dist = poi["_distance"]
        
        # 距离显示优化: <1km 显示米，>1km 显示千米
        if dist == float('inf'):
            dist_str = "未知距离"
        elif dist < 1:
            dist_str = f"{int(dist * 1000)}m"
        else:
            dist_str = f"{dist:.1f}km"
            
        rating = poi.get("biz_ext", {}).get("rating", "无评分")
        address = poi.get("address", "无地址")
        
        line = f"{i}. {name} | 📏 {dist_str} | ⭐ {rating}\n   📍 {address}"
        result_lines.append(line)

    return "\n".join(result_lines)
