"""
Day 3.3 终极实验: 运行完整的 HelloAgent 🤖
测试 Orchestrator 的状态管理能力（记忆力）。
"""

from orchestrator import SimpleOrchestrator

def main():
    print("=" * 60)
    print("🤖 HelloAgent (Phase 3 Final Version)")
    print("输入 'exit' 或 'quit' 退出")
    print("=" * 60)
    
    agent = SimpleOrchestrator()
    
    # 模拟一段多轮对话
    # 场景: 用户先查天气，然后基于上下文查景点
    
    test_inputs = [
        "你好",
        "帮我查查北京的天气",
        "那上海呢？",  # <--- 关键测试点！它能利用上下文知道你在问天气吗？
        "上海有哪些好吃的必胜客？", 
        "exit"
    ]
    
    # 自动运行测试
    print("\n[自动测试模式]")
    for user_input in test_inputs:
        if user_input in ["exit", "quit"]:
            break
            
        agent.chat(user_input)
        print("-" * 40)

if __name__ == "__main__":
    main()
