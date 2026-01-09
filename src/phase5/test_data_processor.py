"""
Phase 5.2 测试: 数据清洗与排序 🧪
"""

from data_processor import process_pois

def test_sorting():
    print("=" * 60)
    print("🧹 Data Processor 测试")
    print("=" * 60)
    
    # 模拟用户位置: 北京天安门
    # 39.9087, 116.3975
    user_lat, user_lon = 39.9087, 116.3975
    
    # 模拟高德 API 返回的乱序 POI 数据
    mock_pois = [
        {
            "name": "北京南站 (远)",
            "location": "116.3790,39.8651", # 约 5km
            "address": "丰台区",
            "biz_ext": {"rating": "4.5"}
        },
        {
            "name": "故宫博物院 (近)",
            "location": "116.3970,39.9180", # 约 1km
            "address": "东城区",
            "biz_ext": {"rating": "5.0"}
        },
        {
            "name": "天坛公园 (中)", 
            "location": "116.4108,39.8837", # 约 3km
            "address": "东城区",
            "biz_ext": {"rating": "4.8"}
        }
    ]
    
    print(f"📍 用户位置: {user_lat}, {user_lon}")
    print("处理中...\n")
    
    result = process_pois(mock_pois, user_lat, user_lon)
    
    print("✅ 排序结果:")
    print(result)
    
    # 验证逻辑: 故宫必须排第一
    if "1. 故宫" in result:
        print("\n🎉 测试通过: 最近的地点排在了第一位")
    else:
        print("\n❌ 测试失败: 排序不正确")

if __name__ == "__main__":
    test_sorting()
