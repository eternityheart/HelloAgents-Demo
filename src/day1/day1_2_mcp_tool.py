"""
Day 1.2 实验: 你的第一个 MCP 工具

🧒 小学生讲解:
这个文件就像是一个"工具箱"，里面装着几个工具:
- add: 加法计算器
- multiply: 乘法计算器
- get_weather: 天气查询 (模拟)

这些工具通过 MCP 协议暴露出去，Agent 就可以"借用"它们了。

🎓 面试话术:
"我使用 FastMCP 框架封装工具，通过 @mcp.tool() 装饰器将普通函数
转换为 MCP 工具。函数的 docstring 会被 LLM 用来理解工具的用途。"
"""

from mcp.server.fastmcp import FastMCP

# ========================================
# Step 1: 创建 MCP 服务器
# ========================================
# "Calculator" 是这个工具箱的名字
mcp = FastMCP("Calculator")


# ========================================
# Step 2: 定义工具 - 加法
# ========================================
@mcp.tool()
def add(a: int, b: int) -> int:
    """
    把两个数字加起来
    
    Args:
        a: 第一个数字
        b: 第二个数字
    
    Returns:
        两个数字的和
    """
    print(f"🔧 工具被调用: add({a}, {b})")  # 调试信息
    result = a + b
    print(f"📤 返回结果: {result}")
    return result


# ========================================
# Step 3: 定义工具 - 乘法
# ========================================
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """
    把两个数字相乘
    
    Args:
        a: 第一个数字
        b: 第二个数字
    
    Returns:
        两个数字的乘积
    """
    print(f"🔧 工具被调用: multiply({a}, {b})")
    result = a * b
    print(f"📤 返回结果: {result}")
    return result


# ========================================
# Step 4: 定义工具 - 模拟天气查询
# ========================================
@mcp.tool()
def get_weather(city: str) -> str:
    """
    查询指定城市的天气 (模拟数据)
    
    Args:
        city: 城市名称，如 "北京"
    
    Returns:
        天气描述字符串
    """
    print(f"🔧 工具被调用: get_weather('{city}')")
    
    # 模拟数据 (后续会换成真实的高德API)
    weather_data = {
        "北京": "晴天，气温 -2°C ~ 8°C",
        "上海": "多云，气温 5°C ~ 12°C",
        "广州": "小雨，气温 15°C ~ 22°C",
    }
    
    result = weather_data.get(city, f"{city}的天气数据暂无")
    print(f"📤 返回结果: {result}")
    return result


# ========================================
# Step 5: 测试代码 - 直接运行验证
# ========================================
if __name__ == "__main__":
    print("=" * 50)
    print("🧪 MCP 工具测试")
    print("=" * 50)
    print()
    
    # 测试加法
    print("测试 1: add(3, 5)")
    result1 = add(3, 5)
    print(f"期望: 8, 实际: {result1}, {'✅ 通过' if result1 == 8 else '❌ 失败'}")
    print()
    
    # 测试乘法
    print("测试 2: multiply(4, 7)")
    result2 = multiply(4, 7)
    print(f"期望: 28, 实际: {result2}, {'✅ 通过' if result2 == 28 else '❌ 失败'}")
    print()
    
    # 测试天气
    print("测试 3: get_weather('北京')")
    result3 = get_weather("北京")
    print(f"结果: {result3}")
    print()
    
    print("=" * 50)
    print("🎉 所有测试完成!")
    print("=" * 50)
