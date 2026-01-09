"""
Day 3.2 实验: 结构化输出验证
展示如何将 LLM 的 JSON 字符串仅仅转换为 Python 字典，
而是转换为强类型的 Pydantic 对象。
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from system_prompts import get_orchestrator_prompt
from models import AgentAction, AgentResponse

# 代理设置
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def parse_llm_output(json_str: str):
    """尝试将 JSON 字符串解析为 Pydantic 对象"""
    try:
        data = json.loads(json_str)
        msg_type = data.get("type")
        
        if msg_type == "tool_call":
            # 自动验证字段类型（例如 args 必须是 dict）
            action = AgentAction(**data)
            print(f"✅ 成功解析为 [AgentAction]")
            print(f"   工具: {action.tool_name}")
            print(f"   参数: {action.args}")
            print(f"   思考: {action.thought}")
            return action
            
        elif msg_type == "response":
            response = AgentResponse(**data)
            print(f"✅ 成功解析为 [AgentResponse]")
            print(f"   回复: {response.content}")
            print(f"   思考: {response.thought}")
            return response
            
        else:
            print(f"❌ 未知消息类型: {msg_type}")
            
    except Exception as e:
        print(f"❌ Pydantic 校验失败: {e}")
        # 在真实 Agent 中，这里会触发 Retry 机制，把错误扔回给 LLM 让它重写

def test_structured_output(user_query: str):
    print(f"\n👤 用户: {user_query}")
    print("-" * 40)
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": get_orchestrator_prompt()},
            {"role": "user", "content": user_query}
        ],
        response_format={"type": "json_object"},
        temperature=0.1
    )
    
    content = response.choices[0].message.content
    print(f"📦 原始 JSON: {content}")
    print("-" * 20)
    
    # 解析验证
    parse_llm_output(content)

if __name__ == "__main__":
    print("Typer Pydantic 结构化测试")
    
    # 1. 测试工具调用
    test_structured_output("帮我查查广州的小蛮腰门票多少钱？")
    
    # 2. 测试直接回复
    test_structured_output("这就去。")
