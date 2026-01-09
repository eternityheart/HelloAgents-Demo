"""
Phase 4.1 测试: 直接调用 Scout Agent 函数
验证 FastMCP 封装下的函数逻辑是否正常。
"""

import asyncio
from scout_agent import _search_poi_logic

def test_scout_logic():
    print("=" * 60)
    print("🔭 Scout Agent 逻辑测试 (Direct Import)")
    print("=" * 60)
    
    # 直接调用分离出来的逻辑函数
    
    # Case 1: 搜索北京故宫
    print("1. 搜索 '北京 故宫 (景点)'...")
    result1 = _search_poi_logic(city="北京", keyword="故宫", poi_type="景点")
    print(result1)
    print("-" * 40)
    
    # Case 2: 搜索上海必胜客
    print("2. 搜索 '上海 必胜客 (餐厅)'...")
    result2 = _search_poi_logic(city="上海", keyword="必胜客", poi_type="餐厅")
    print(result2)
    print("-" * 40)
    
    if "API错误" in result1 or "API错误" in result2:
        print("❌ 测试失败: API 返回错误")
    else:
        print("✅ 测试通过: 逻辑正常")

if __name__ == "__main__":
    test_scout_logic()
