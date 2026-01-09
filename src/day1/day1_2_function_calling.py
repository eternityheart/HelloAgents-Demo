"""
Day 1.2 实验（进阶）: 让 LLM 自己决定调用哪个工具

🧒 小学生讲解:
之前我们手动调用了 add() 和 get_weather() 函数。
现在我们要让 LLM 自己判断：用户问"3加5等于多少？"时，
它会自动选择调用 add 工具！

🎓 面试话术:
"Function Calling 是一个两阶段流程：
 1. 第一阶段：LLM 分析用户意图，决定是否需要工具、需要哪个工具
 2. 第二阶段：执行工具，把结果反馈给 LLM，生成最终回答"
"""

import os
import json

# 设置代理（如需）
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


# ========================================
# Step 1: 定义工具（给 LLM 看的"说明书"）
# ========================================
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "把两个数字加起来，返回它们的和",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "第一个数字"},
                    "b": {"type": "integer", "description": "第二个数字"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称，如北京、上海"}
                },
                "required": ["city"]
            }
        }
    }
]


# ========================================
# Step 2: 工具实现（真正干活的代码）
# ========================================
def add(a: int, b: int) -> int:
    print(f"  🔧 [工具执行] add({a}, {b})")
    return a + b

def get_weather(city: str) -> str:
    print(f"  🔧 [工具执行] get_weather('{city}')")
    weather_data = {
        "北京": "晴天，气温 -2°C ~ 8°C",
        "上海": "多云，气温 5°C ~ 12°C",
        "广州": "小雨，气温 15°C ~ 22°C",
    }
    return weather_data.get(city, f"{city}的天气数据暂无")


# ========================================
# Step 3: 核心流程 - Function Calling
# ========================================
def chat_with_tools(user_message: str):
    """
    让 LLM 根据用户输入，自动决定是否调用工具
    """
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )
    
    print(f"\n👤 用户: {user_message}")
    print("-" * 50)
    
    # ======== 第一阶段: LLM 分析意图 ========
    print("📡 第一阶段: 发送给 LLM，让它决定是否需要工具...")
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个智能助手，可以使用工具来回答问题。"},
            {"role": "user", "content": user_message}
        ],
        tools=TOOLS,
        tool_choice="auto"  # 让 LLM 自己决定
    )
    
    message = response.choices[0].message
    
    # 检查 LLM 是否决定调用工具
    if message.tool_calls:
        print(f"🤖 LLM 决定调用工具!")
        
        # ======== 第二阶段: 执行工具 ========
        tool_results = []
        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            
            print(f"  📋 工具名称: {func_name}")
            print(f"  📋 工具参数: {func_args}")
            
            # 根据名称调用对应函数
            if func_name == "add":
                result = add(**func_args)
            elif func_name == "get_weather":
                result = get_weather(**func_args)
            else:
                result = "未知工具"
            
            tool_results.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "content": str(result)
            })
        
        # ======== 第三阶段: 把结果反馈给 LLM ========
        print("📡 第三阶段: 把工具结果反馈给 LLM...")
        
        final_response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个智能助手。"},
                {"role": "user", "content": user_message},
                message,  # LLM 的工具调用请求
                *tool_results  # 工具执行结果
            ]
        )
        
        final_answer = final_response.choices[0].message.content
    else:
        # LLM 决定不需要工具，直接回答
        print("🤖 LLM 决定直接回答（不需要工具）")
        final_answer = message.content
    
    print("-" * 50)
    print(f"🤖 最终回答: {final_answer}")
    return final_answer


# ========================================
# Step 4: 测试
# ========================================
if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Function Calling 演示")
    print("=" * 60)
    
    # 测试 1: 需要调用加法工具
    print("\n" + "=" * 60)
    print("测试 1: 问数学问题（应该调用 add 工具）")
    print("=" * 60)
    chat_with_tools("请帮我计算 15 加 27 等于多少？")
    
    # 测试 2: 需要调用天气工具
    print("\n" + "=" * 60)
    print("测试 2: 问天气（应该调用 get_weather 工具）")
    print("=" * 60)
    chat_with_tools("北京今天天气怎么样？")
    
    # 测试 3: 不需要工具
    print("\n" + "=" * 60)
    print("测试 3: 普通问题（不需要工具）")
    print("=" * 60)
    chat_with_tools("你好，介绍一下你自己")
    
    print("\n" + "=" * 60)
    print("🎉 演示完成!")
    print("=" * 60)
