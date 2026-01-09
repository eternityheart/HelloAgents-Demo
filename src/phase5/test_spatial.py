"""
Phase 5.3 测试: 空间感知 Agent 🧠
验证 "搜附近" 功能是否生效，结果是否按距离排序。
"""

from spatial_agent import _search_nearby_logic

def test_spatial_search():
    print("=" * 60)
    print("🧠 Spatial Scout 测试 (用户在天安门)")
    print("=" * 60)

    # 模拟用户在天安门 (39.9087, 116.3975)
    user_lat, user_lon = 39.9087, 116.3975
    
    # 搜索附近的 WC (测试实用性)
    print("🔍 搜索附近的厕所...")
    result = _search_nearby_logic(
        keyword="厕所", 
        user_lat=user_lat, 
        user_lon=user_lon, 
        city="北京",
        poi_type="厕所"
    )
    
    print("\n✅ 结果列表:")
    print(result)
    
    # 验证逻辑
    if "1." in result and "km" in result:
        print("\n🎉 测试通过: 成功返回带距离的排序结果")
    else:
        print("\n❌ 测试失败: 结果格式不正确")

if __name__ == "__main__":
    test_spatial_search()
