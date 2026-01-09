"""
Phase 4.3: Concierge Agent (礼宾员/Orchestrator) 🛎️
这是本阶段的集大成者。
它是一个 MCP Client，负责连接并调度 Scout 和 Meteorologist。
"""

import os
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

class ConciergeAgent:
    def __init__(self):
        self.openai = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        self.messages = [
            {"role": "system", "content": """
你是一个全能的礼宾员 (Concierge)。
你有两个得力助手：
1. Scout (侦察兵): 负责搜索地点信息
2. Meteorologist (气象员): 负责查询天气

请根据用户需求，调度合适的工具。
必须输出 JSON 格式：
{
    "type": "tool_call",
    "tool_name": "...",
    "args": { ... },
    "thought": "..."
}
或者
{
    "type": "response",
    "content": "...",
    "thought": "..."
}
"""}
        ]
        # 保存所有连接的 Session
        self.exit_stack = AsyncExitStack()
        self.sessions = {} # {server_name: session}
        self.tools_map = {} # {tool_name: (server_name, tool_obj)}

    async def connect_to_server(self, name: str, script_path: str):
        """连接到一个 MCP Server"""
        print(f"🔌 Connecting to {name}...", end="", flush=True)
        
        server_params = StdioServerParameters(
            command="python",
            args=[script_path],
            env=os.environ.copy() # 传递环境变量 (API Key)
        )
        
        # 使用 ExitStack 管理上下文，确保程序退出时自动关闭连接
        transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        read, write = transport
        session = await self.exit_stack.enter_async_context(ClientSession(read, write))
        
        await session.initialize()
        self.sessions[name] = session
        
        # 获取工具列表
        tools_result = await session.list_tools()
        for tool in tools_result.tools:
            self.tools_map[tool.name] = (name, tool)
            print(f"\n   Found tool: {tool.name}", end="")
            
        print(" ✅")

    async def run(self):
        """启动 Agent"""
        try:
            # 1. 连接子 Agents (相对路径需要注意，这里假设在项目根目录运行)
            await self.connect_to_server("Scout", "src/phase4/scout_agent.py")
            await self.connect_to_server("Meteorologist", "src/phase4/weather_agent.py")
            
            print("\n🛎️ Concierge is ready! (Type 'quit' to exit)")
            
            # 2. 对话循环
            while True:
                user_msg = input("\n👤 You: ")
                if user_msg.lower() in ["quit", "exit"]:
                    break
                    
                self.messages.append({"role": "user", "content": user_msg})
                
                # 3. 询问 LLM
                print("🧠 Thinking...", end="", flush=True)
                # 为了简化代码，这里省略了把 tool definitions 动态生成 Prompt 的步骤
                # 在生产环境中，应该遍历 self.tools_map 生成 TOOL_DEFINITIONS
                
                response = self.openai.chat.completions.create(
                    model="deepseek-chat",
                    messages=self.messages,
                    response_format={"type": "json_object"},
                    temperature=0
                )
                print(" Done!")
                
                content = response.choices[0].message.content
                
                try:
                    data = json.loads(content)
                    if data["type"] == "response":
                        print(f"🤖 Agent: {data['content']}")
                        self.messages.append({"role": "assistant", "content": data["content"]})
                        
                    elif data["type"] == "tool_call":
                        t_name = data["tool_name"]
                        t_args = data["args"]
                        print(f"🛠️ Call {t_name}({t_args})")
                        
                        if t_name in self.tools_map:
                            server_name, _ = self.tools_map[t_name]
                            session = self.sessions[server_name]
                            
                            # ---> 真正跨进程调用 MCP 工具 <---
                            result = await session.call_tool(t_name, arguments=t_args)
                            
                            # MCP 返回的是一个 list[TextContent | ImageContent]
                            tool_out_text = result.content[0].text
                            print(f"✅ Result:\n{tool_out_text}")
                            
                            self.messages.append({
                                "role": "user",
                                "content": f"Tool {t_name} Result:\n{tool_out_text}"
                            })
                            
                            # 再次思考 (Re-Act)
                            # (此处省略 Re-Act 逻辑以保持 Demo 简洁，实际应递归调用)
                            
                        else:
                            print(f"❌ Error: Unknown tool {t_name}")
                            
                except Exception as e:
                    print(f"❌ Error: {e}\nRaw: {content}")

        finally:
            print("\n🔌 Closing connections...")
            await self.exit_stack.aclose()

if __name__ == "__main__":
    agent = ConciergeAgent()
    asyncio.run(agent.run())
