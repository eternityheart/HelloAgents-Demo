"""
Phase 5.1: Geospatial Utilities 📏
提供地理空间计算的基础工具。

核心功能:
1. Haversine 公式: 计算地球表面两点间的球面距离
2. 坐标格式化: 统一处理经纬度字符串
"""

import math
from typing import Tuple

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    计算两点经纬度之间的球面距离 (单位: 千米)
    
    Args:
        lat1, lon1: 起点纬度, 经度
        lat2, lon2: 终点纬度, 经度
        
    Returns:
        float: 距离 (千米)，保留2位小数
    """
    R = 6371  # 地球平均半径 (km)

    # 将角度转换为弧度
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Haversine 公式
    a = math.sin(delta_phi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2)**2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return round(distance, 2)

def parse_location(loc_str: str) -> Tuple[float, float]:
    """
    解析高德 API 返回的坐标字符串 "lon,lat"
    注意: 高德返回顺序是 (经度, 纬度) -> (lon, lat)
    我们通常习惯 (lat, lon)
    """
    try:
        parts = loc_str.split(",")
        if len(parts) != 2:
            return (0.0, 0.0)
        
        lon = float(parts[0])
        lat = float(parts[1])
        return (lat, lon)
    except Exception:
        return (0.0, 0.0)

if __name__ == "__main__":
    # 简单测试
    # 北京天安门 (39.9087, 116.3975)
    # 上海东方明珠 (31.2397, 121.4939)
    d = haversine_distance(39.9087, 116.3975, 31.2397, 121.4939)
    print(f"北京到上海的直线距离约: {d} km")
