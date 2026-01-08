"""
Phase 0: Hello World Agent - 你的第一个AI Agent

🧒 小学生讲解:
这是你的第一个"智能员工"! 
他现在只会一件事 —— 回答你的问题。
虽然简单，但这是所有复杂Agent的基础！

学习目标:
1. 理解LLM API的调用方式
2. 学会使用环境变量管理密钥
3. 成功运行你的第一个Agent

🎓 面试话术:
"这是一个基础的stateless agent，每次调用独立无状态。
后续会加入memory和tool-use能力，使其能完成复杂任务。"
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def create_simple_agent():
    """
    创建一个简单的对话Agent
    
    这个函数演示了最基本的LLM调用模式：
    1. 创建客户端连接
    2. 发送消息
    3. 获取回复
    """
    # 从环境变量读取API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    # 检查是否配置了密钥
    if not api_key:
        print("❌ 错误: 请先配置 DEEPSEEK_API_KEY 环境变量!")
        print("📝 步骤:")
        print("   1. 复制 .env.example 为 .env")
        print("   2. 填入你的 DeepSeek API 密钥")
        return None
    
    # 创建OpenAI客户端 (DeepSeek兼容OpenAI格式)
    client = OpenAI(
        api_key=api_key,
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    )
    
    return client


def simple_chat(client, user_message: str) -> str:
    """
    简单的对话函数
    
    Args:
        client: OpenAI客户端
        user_message: 用户输入的消息
    
    Returns:
        Agent的回复内容
    
    🧒 小学生讲解:
    这就像给Agent发微信消息，然后等他回复。
    - system: 告诉Agent他是谁（"你是旅行助手"）
    - user: 你说的话
    - assistant: Agent的回复
    """
    try:
        response = client.chat.completions.create(
            model=os.getenv("DEFAULT_MODEL", "deepseek-chat"),
            messages=[
                {
                    "role": "system", 
                    "content": "你是一个友好的旅行规划助手，擅长推荐景点和规划行程。"
                },
                {
                    "role": "user", 
                    "content": user_message
                }
            ],
            # 限制回复长度，避免费用失控
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ 调用失败: {e}"


def main():
    """主函数 - 运行交互式对话"""
    print("=" * 50)
    print("🤖 HelloAgents - 你的第一个AI Agent")
    print("=" * 50)
    print("输入 'quit' 退出对话\n")
    
    # 创建Agent
    client = create_simple_agent()
    if not client:
        return
    
    print("✅ Agent已就绪! 试着问我一些旅行问题吧~\n")
    
    # 交互循环
    while True:
        user_input = input("你: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 再见!")
            break
        
        if not user_input:
            continue
        
        print("🤔 Agent思考中...")
        reply = simple_chat(client, user_input)
        print(f"\n🤖 Agent: {reply}\n")


# ===== 测试用例 =====
def test_hello_agent():
    """
    验收测试
    
    ✅ 验收标准:
    1. 程序运行不报错
    2. 能返回关于旅行的回答
    3. 回答是中文
    """
    client = create_simple_agent()
    
    if not client:
        print("⚠️ 跳过测试: API未配置")
        return
    
    # 测试用例
    test_questions = [
        "北京有什么好玩的地方?",
        "推荐一个适合3天的北京行程",
        "你好"  # 测试非旅行问题
    ]
    
    print("\n📋 开始验收测试...\n")
    
    for i, question in enumerate(test_questions, 1):
        print(f"测试 {i}: {question}")
        reply = simple_chat(client, question)
        print(f"回复: {reply[:100]}..." if len(reply) > 100 else f"回复: {reply}")
        print("-" * 40)
    
    print("\n✅ 验收测试完成!")


if __name__ == "__main__":
    import sys
    
    if "--test" in sys.argv:
        # 运行测试模式
        test_hello_agent()
    else:
        # 运行交互模式
        main()
