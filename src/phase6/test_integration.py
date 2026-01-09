"""
Phase 6.2 测试: 集成测试 (Sync Client -> Async Server)
模拟真实用户提问，验证 Orchestrator 在后端是否正常工作。
"""

import requests
import json

def test_integration():
    print("=" * 60)
    print("🧠 API 集成测试 (POST /chat/stream)")
    print("=" * 60)
    
    url = "http://127.0.0.1:8000/chat/stream"
    payload = {"message": "帮我查查北京的天气，顺便看看附近的烤鸭店"}
    
    print(f"👤 User: {payload['message']}")
    print("⏳ Waiting for stream...\n")
    
    try:
        with requests.post(url, json=payload, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    decoded = line.decode("utf-8")
                    if decoded.startswith("data: "):
                        content = decoded[6:]
                        if content == "[DONE]":
                            print("\n\n[会话结束]")
                            break
                        # 实时打印
                        print(content, end="", flush=True)
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        print("请确认 server 是否在运行: python src/phase6/main.py")

if __name__ == "__main__":
    test_integration()
