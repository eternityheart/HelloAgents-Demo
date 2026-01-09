"""
Day 3.1 实验: 测试 Prompt Engineering 效果
验证 LLM 是否能遵守我们在 system_prompts.py 中定义的协议。
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from system_prompts import get_orchestrator_prompt

# 代理设置
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def test_prompt(user_query: str):
    print(f"\n👤 用户: {user_query}")
    print("-" * 40)
    
    # 获取我们设计的专业 Prompt
    system_prompt = get_orchestrator_prompt()
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            response_format={"type": "json_object"}, # 强制 JSON 模式
            temperature=0.1 # 低温度，更稳定
        )
        
        content = response.choices[0].message.content
        
        # 尝试解析 JSON
        data = json.loads(content)
        print("🤖 LLM 输出 (JSON):")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # 简单的验证逻辑
        if data.get("type") == "tool_call":
            print(f"✅ 成功识别工具: {data['tool_name']}")
        elif data.get("type") == "response":
            print(f"✅ 成功识别闲聊")
        else:
            print("⚠️ 未知类型")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        print(f"原始返回: {content if 'content' in locals() else 'None'}")

if __name__ == "__main__":
    print("🧪 Prompt Engineering 测试")
    
    # 1. 测试闲聊
    test_prompt("你好，你是谁？")
    
    # 2. 测试工具调用
    test_prompt("帮我查查北京的天气")
    
    # 3. 测试复杂一点的
    test_prompt("我想去上海玩，帮我搜一下附近的迪士尼酒店")
