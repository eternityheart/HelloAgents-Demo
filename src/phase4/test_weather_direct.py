"""
Phase 4.2 测试: 气象员逻辑测试
验证 input validation 和 robustness。
"""

from weather_agent import _get_weather_logic

def test_weather_logic():
    print("=" * 60)
    print("🌤️ Meteorologist Agent 逻辑测试")
    print("=" * 60)
    
    # Case 1: 正常查询 (北京)
    print("1. 查询 '北京'...")
    res1 = _get_weather_logic("北京")
    print(res1)
    print("-" * 40)
    
    # Case 2: 正常查询 (带'市'字)
    print("2. 查询 '上海市' (测试自动清洗)...")
    res2 = _get_weather_logic("上海市")
    print(res2)
    print("-" * 40)
    
    # Case 3: 不支持的城市 (纽约)
    print("3. 查询 '纽约' (测试参数校验)...")
    res3 = _get_weather_logic("纽约")
    print(res3)
    print("-" * 40)
    
    # 验证逻辑
    if "天气实况" in res1 and "天气实况" in res2:
        if "不支持查询" in res3:
            print("✅ 测试通过: 正常查询和错误拦截都符合预期")
        else:
            print("❌ 测试失败: 未拦截不支持的城市")
    else:
         print("❌ 测试失败: 正常查询未返回天气数据")

if __name__ == "__main__":
    test_weather_logic()
