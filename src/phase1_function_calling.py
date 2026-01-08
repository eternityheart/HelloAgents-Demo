"""
Phase 1: Function Calling - 让Agent学会使用工具

🧒 小学生讲解:
之前的Agent只会"说话"，现在要教他"干活"！
就像给员工发一个工具清单，告诉他："遇到这种问题，用这个工具"。

比如用户问"北京天气怎么样？"：
1. Agent看清单："哦，我有'查天气'这个工具"
2. Agent使用工具：调用get_weather("北京")
3. Agent得到结果："晴天，25度"
4. Agent回答用户："北京今天天气不错，晴天25度"

学习目标:
1. 理解Function Calling机制
2. 学会定义工具的JSON Schema
3. 掌握两阶段对话流程（决策→执行→反馈）

🎓 面试话术:
"OpenAI的Function Calling通过将工具定义注入prompt，
让LLM输出结构化的函数调用请求。我的实现采用ReAct模式：
先让LLM决策调用哪个工具，执行后再反馈结果给LLM生成最终回答。"
"""

from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from typing import Callable, Dict, Any

load_dotenv()


# ===== Step 1: 定义工具（Tools） =====
# 这些是Agent可以使用的"能力"

def get_weather(city: str) -> Dict[str, Any]:
    """
    模拟天气查询工具
    
    🧒 小学生讲解:
    现在是假数据，后面会接真实的高德天气API
    """
    fake_weather_db = {
        "北京": {"city": "北京", "weather": "晴天", "temperature": 25, "humidity": 40},
        "上海": {"city": "上海", "weather": "多云", "temperature": 28, "humidity": 65},
        "广州": {"city": "广州", "weather": "小雨", "temperature": 30, "humidity": 80},
        "成都": {"city": "成都", "weather": "阴天", "temperature": 22, "humidity": 55},
    }
    return fake_weather_db.get(city, {"city": city, "weather": "未知", "temperature": 0, "humidity": 0})


def search_attractions(city: str, category: str = "景点") -> Dict[str, Any]:
    """
    模拟景点搜索工具
    
    后面会接高德地图POI搜索API
    """
    fake_attraction_db = {
        "北京": {
            "景点": ["故宫", "长城", "天坛", "颐和园", "圆明园"],
            "美食": ["全聚德烤鸭", "护国寺小吃", "簋街"],
            "购物": ["王府井", "三里屯"],
        },
        "上海": {
            "景点": ["外滩", "东方明珠", "豫园", "迪士尼"],
            "美食": ["南翔小笼包", "生煎", "本帮菜"],
        }
    }
    city_data = fake_attraction_db.get(city, {})
    attractions = city_data.get(category, [])
    return {"city": city, "category": category, "attractions": attractions}


# ===== Step 2: 工具定义的JSON Schema =====
# 这是告诉LLM"你有哪些工具可用"的格式

TOOLS_DEFINITION = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的当前天气信息，包括天气状况、温度和湿度",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如'北京'、'上海'"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function", 
        "function": {
            "name": "search_attractions",
            "description": "搜索指定城市的景点、美食或购物地点",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    },
                    "category": {
                        "type": "string",
                        "description": "搜索类别：景点、美食、购物",
                        "enum": ["景点", "美食", "购物"]
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# 工具函数映射（名称 -> 函数）
TOOL_FUNCTIONS: Dict[str, Callable] = {
    "get_weather": get_weather,
    "search_attractions": search_attractions,
}


# ===== Step 3: Agent核心逻辑 =====

class FunctionCallingAgent:
    """
    支持工具调用的Agent
    
    🧒 工作流程:
    用户提问 → LLM决策(用什么工具?) → 执行工具 → LLM总结回答
    """
    
    def __init__(self):
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("请配置 DEEPSEEK_API_KEY 环境变量")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        )
        self.model = os.getenv("DEFAULT_MODEL", "deepseek-chat")
    
    def chat(self, user_message: str) -> str:
        """
        与用户对话，支持自动调用工具
        
        这是两阶段对话流程的完整实现
        """
        print(f"\n📝 用户: {user_message}")
        
        # ===== 第一阶段: 让LLM决定要不要用工具 =====
        messages = [
            {
                "role": "system",
                "content": """你是一个智能旅行助手。
当用户询问天气时，使用 get_weather 工具获取数据。
当用户询问景点、美食或购物时，使用 search_attractions 工具。
如果用户的问题不需要工具，直接回答即可。"""
            },
            {"role": "user", "content": user_message}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=TOOLS_DEFINITION,
            tool_choice="auto"  # 让LLM自己决定是否使用工具
        )
        
        assistant_message = response.choices[0].message
        
        # ===== 检查LLM是否想使用工具 =====
        if not assistant_message.tool_calls:
            # 不需要工具，直接返回回答
            print("💬 Agent直接回答（无需工具）")
            return assistant_message.content
        
        # ===== 第二阶段: 执行工具并反馈结果 =====
        print(f"🔧 Agent决定使用工具...")
        
        # 把LLM的工具调用请求加入对话历史
        messages.append(assistant_message)
        
        # 处理每个工具调用
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"   → 调用: {function_name}({function_args})")
            
            # 执行真实的工具函数
            if function_name in TOOL_FUNCTIONS:
                result = TOOL_FUNCTIONS[function_name](**function_args)
                result_str = json.dumps(result, ensure_ascii=False)
            else:
                result_str = json.dumps({"error": f"未知工具: {function_name}"})
            
            print(f"   ← 结果: {result_str}")
            
            # 把工具结果加入对话历史
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result_str
            })
        
        # ===== 第三阶段: 让LLM根据工具结果生成最终回答 =====
        final_response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        
        final_answer = final_response.choices[0].message.content
        print(f"✅ Agent最终回答已生成")
        
        return final_answer


# ===== 测试代码 =====
def main():
    """交互式测试"""
    print("=" * 60)
    print("🔧 Phase 1: Function Calling Agent")
    print("=" * 60)
    print("我现在会使用工具了! 试着问我:")
    print("  - 北京今天天气怎么样?")
    print("  - 上海有什么好玩的景点?")
    print("  - 成都有什么好吃的?")
    print("输入 'quit' 退出\n")
    
    agent = FunctionCallingAgent()
    
    while True:
        user_input = input("\n你: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 再见!")
            break
        if not user_input:
            continue
        
        reply = agent.chat(user_input)
        print(f"\n🤖 Agent: {reply}")


def test_function_calling():
    """
    验收测试
    
    ✅ 验收标准:
    1. 问天气时，能看到调用 get_weather
    2. 问景点时，能看到调用 search_attractions
    3. 闲聊时，不调用任何工具
    """
    print("\n📋 开始 Function Calling 验收测试...\n")
    
    try:
        agent = FunctionCallingAgent()
    except ValueError as e:
        print(f"⚠️ 跳过测试: {e}")
        return
    
    test_cases = [
        ("北京今天天气怎么样?", "应该调用get_weather"),
        ("上海有什么好玩的地方?", "应该调用search_attractions"),
        ("你好，请问你是谁?", "应该直接回答，不调用工具"),
    ]
    
    for question, expected in test_cases:
        print(f"\n{'='*50}")
        print(f"测试: {question}")
        print(f"期望: {expected}")
        print("-" * 50)
        
        reply = agent.chat(question)
        print(f"\n回复: {reply[:200]}..." if len(reply) > 200 else f"\n回复: {reply}")
    
    print(f"\n{'='*50}")
    print("✅ 验收测试完成!")


if __name__ == "__main__":
    import sys
    
    if "--test" in sys.argv:
        test_function_calling()
    else:
        main()
