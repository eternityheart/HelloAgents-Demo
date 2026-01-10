"""
Hotel Agent 直接测试脚本
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phase4.hotel_agent import search_hotel, get_hotels

def test_basic_search():
    """测试基本搜索"""
    print("=" * 50)
    print("测试1: 北京酒店基本搜索")
    print("=" * 50)
    result = search_hotel("北京")
    print(result)
    print()

def test_keyword_search():
    """测试关键词搜索"""
    print("=" * 50)
    print("测试2: 北京五星级酒店")
    print("=" * 50)
    result = search_hotel("北京", "五星级酒店", min_rating=4.0)
    print(result)
    print()

def test_rating_filter():
    """测试评分过滤"""
    print("=" * 50)
    print("测试3: 上海高评分酒店 (≥4.5)")
    print("=" * 50)
    result = search_hotel("上海", "酒店", min_rating=4.5, max_results=3)
    print(result)
    print()

def test_simple_interface():
    """测试简化接口"""
    print("=" * 50)
    print("测试4: 简化接口 get_hotels")
    print("=" * 50)
    result = get_hotels("杭州", "西湖景区酒店")
    print(result)
    print()

if __name__ == "__main__":
    test_basic_search()
    test_keyword_search()
    test_rating_filter()
    test_simple_interface()
    print("✅ 所有测试完成!")
