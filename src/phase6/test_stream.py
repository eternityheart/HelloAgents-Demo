"""
Phase 6.1 测试: SSE 客户端验证
模拟前端浏览器，连接 /stream 接口，展示打字机效果。
"""

import requests
import sys
import time

def test_stream_client():
    print("=" * 60)
    print("🌊 SSE 流式接收测试 (Connecting to http://127.0.0.1:8000/stream)")
    print("=" * 60)
    
    try:
        # stream=True 是关键
        with requests.get("http://127.0.0.1:8000/stream", stream=True) as r:
            for line in r.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    # SSE 格式: "data: <content>"
                    if decoded_line.startswith("data: "):
                        content = decoded_line[6:] # 去掉前缀
                        if content == "[DONE]":
                            print("\n\n[传输结束]")
                            break
                        
                        # 模拟前端渲染：不换行打印
                        print(content, end="", flush=True)
                        
    except Exception as e:
        print(f"\n❌ 连接失败: {e}")
        print("请确保 main.py 已经在一个单独的终端窗口中运行！")

if __name__ == "__main__":
    test_stream_client()
