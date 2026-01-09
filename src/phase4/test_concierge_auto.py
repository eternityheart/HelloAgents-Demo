"""
Phase 4.3 测试: 自动化验证 Concierge Agent 🛎️
模拟用户输入，测试 Orchestrator 是否能正确连接 Scout 和 Meteorologist。
"""

import os
import sys
import json
import asyncio
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI
from dotenv import load_dotenv

# 设置代理
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"

load_dotenv()

class AutoConcierge:
    def __init__(self):
        self.openai = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        # 注意：这里我们手动把工具定义放进去，模拟"动态发现"后的结果
        # 在更高级的实现中，这些应该通过 session.list_tools() 自动生成
        self.messages = [
            {"role": "system", "content": """
你是一个全能的礼宾员 (Concierge)。
你有以下工具：
1. search_poi(city, keyword, poi_type) - 搜索地点
2. get_weather(city) - 查询天气

请根据用户需求，调度合适的工具。
必须输出 JSON 格式：
{"type": "tool_call", "tool_name": "...", "args": { ... }, "thought": "..."}
或者
{"type": "response", "content": "...", "thought": "..."}
"""}
        ]
        self.exit_stack = AsyncExitStack()
        self.sessions = {} 
        self.tools_map = {}

    async def connect_to_server(self, name: str, script_path: str):
        print(f"🔌 Connecting to {name}...", end="", flush=True)
        server_params = StdioServerParameters(
            command=sys.executable, # 使用当前 venv 的 python
            args=[script_path],
            env=os.environ.copy()
        )
        try:
            transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            read, write = transport
            session = await self.exit_stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
            self.sessions[name] = session
            
            tools_result = await session.list_tools()
            for tool in tools_result.tools:
                self.tools_map[tool.name] = (name, tool)
                print(f" [Found: {tool.name}]", end="")
            print(" ✅")
        except Exception as e:
            print(f" ❌ Failed: {e}")

    async def run_test(self):
        try:
            # 1. 连接服务
            await self.connect_to_server("Scout", "src/phase4/scout_agent.py")
            await self.connect_to_server("Meteorologist", "src/phase4/weather_agent.py")
            
            # 2. 定义测试用例
            test_cases = [
                "帮我查查广州的小蛮腰门票", # 这个应该搜 POI
                "北京今天冷吗？",        # 这个应该查 Weather
                "exit"
            ]
            
            print("\n🚀 开始自动化测试...\n")
            
            for user_msg in test_cases:
                if user_msg == "exit": break
                
                print(f"👤 User: {user_msg}")
                self.messages.append({"role": "user", "content": user_msg})
                
                # Call LLM
                resp = self.openai.chat.completions.create(
                    model="deepseek-chat",
                    messages=self.messages,
                    response_format={"type": "json_object"},
                    temperature=0
                )
                content = resp.choices[0].message.content
                print(f"🧠 LLM: {content}")
                
                data = json.loads(content)
                if data["type"] == "tool_call":
                    t_name = data["tool_name"]
                    if t_name in self.tools_map:
                        server_name, _ = self.tools_map[t_name]
                        print(f"⚡ Dispatching to [{server_name}]...")
                        
                        # Call MCP Tool
                        result = await self.sessions[server_name].call_tool(t_name, arguments=data["args"])
                        print(f"✅ Result: {result.content[0].text[:100]}...") # 只打印前100字
                        
                        # 存入历史 (关键)
                        self.messages.append({"role": "user", "content": f"Result: {result.content[0].text}"})
                    else:
                        print(f"❌ Tool not found: {t_name}")
                
                print("-" * 40)

        finally:
            print("\n🔌 Closing connections...")
            await self.exit_stack.aclose()

if __name__ == "__main__":
    t = AutoConcierge()
    asyncio.run(t.run_test())
