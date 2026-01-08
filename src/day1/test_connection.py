"""
Day 1: 验证"手脑连接"
测试 LLM 是否能正确识别何时调用工具

运行方法:
    python test_connection.py

预期结果:
    LLM 识别出用户想查天气，调用 get_weather 函数
"""

import os
from openai import OpenAI

# ======= 配置区域 =======
# 请替换为你的 DeepSeek API Key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "your-deepseek-key-here")

# ========================


def main():
    print("=" * 50)
    print("🧪 Day 1: 验证 LLM 函数调用能力")
    print("=" * 50)
    
    # 1. 创建 OpenAI 客户端（指向 DeepSeek）
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com"
    )
    
    # 2. 定义一个简单的工具（函数）
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "获取指定城市的当前天气信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称，如：北京、上海"
                        }
                    },
                    "required": ["city"]
                }
            }
        }
    ]
    
    # 3. 测试用户输入
    user_message = "北京明天天气怎么样？"
    print(f"\n📝 用户输入: {user_message}")
    print("-" * 50)
    
    # 4. 调用 LLM
    print("🤖 正在调用 DeepSeek API...")
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": user_message}
            ],
            tools=tools,
            tool_choice="auto"  # 让模型自己决定是否调用工具
        )
        
        # 5. 分析响应
        message = response.choices[0].message
        
        if message.tool_calls:
            print("\n✅ 成功！LLM 识别到需要调用工具：")
            for tool_call in message.tool_calls:
                print(f"   - 函数名: {tool_call.function.name}")
                print(f"   - 参数: {tool_call.function.arguments}")
        else:
            print("\n⚠️ LLM 没有调用工具，直接回复了：")
            print(f"   {message.content}")
            
    except Exception as e:
        print(f"\n❌ 调用失败: {e}")
        print("\n💡 请检查:")
        print("   1. API Key 是否正确")
        print("   2. 网络是否能访问 api.deepseek.com")
    
    print("\n" + "=" * 50)
    print("📌 下一步: 阅读 implementation_plan.md Day 2 部分")
    print("=" * 50)


if __name__ == "__main__":
    main()
