"""
Phase 6.2: Async Orchestrator 🧠
这是 Phase 3 SimpleOrchestrator 的"异步进化版"。
适配 FastAPI 的流式输出 (SSE)。

变化点:
1. OpenAI -> AsyncOpenAI
2. print() -> yield f"data: ..."
3. requests -> asyncio.to_thread(requests)
"""

import os
import json
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

# 复用 Phase 3 的组件
from src.phase3.system_prompts import get_orchestrator_prompt
from src.phase3.models import AgentAction, AgentResponse
from src.phase3.tools import get_weather, search_poi # 这些是 Sync 函数

# 设置代理 (必填，否则 DeepSeek 连不上)
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"

load_dotenv()

class AsyncOrchestrator:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        self.messages = [
            {"role": "system", "content": get_orchestrator_prompt()}
        ]

    async def chat_generator(self, user_input: str):
        """
        生成器函数，用于 SSE 流式输出
        Yields:
            str: SSE formatted string "data: ...\n\n"
        """
        # 1. 记录用户输入
        self.messages.append({"role": "user", "content": user_input})
        
        # 发送思考中状态
        yield "data: 🧠 正在思考...\n\n"
        
        # 2. 调用 LLM (Round 1)
        # 注意: 这里虽然用了 AsyncClient，但暂时没用 stream=True (简化逻辑)
        # 生产环境建议这里也用 stream=True 做 Token 级流式
        try:
            response = await self.client.chat.completions.create(
                model="deepseek-chat",
                messages=self.messages,
                response_format={"type": "json_object"},
                temperature=0.1
            )
        except Exception as e:
            yield f"data: ❌ LLM Error: {str(e)}\n\n"
            return

        llm_content = response.choices[0].message.content
        data = json.loads(llm_content)
        
        # 3. 决策
        msg_type = data.get("type")
        
        if msg_type == "tool_call":
            # ---> 工具调用分支
            action = AgentAction(**data)
            yield f"data: 🛠️ 需要使用工具: {action.tool_name}\n\n"
            yield f"data: 🤔 思考: {action.thought}\n\n"
            
            # 异步执行同步工具 (关键点!)
            # 避免阻塞整个 Event Loop
            tool_result = await self._run_sync_tool(action)
            yield f"data: ✅ 工具执行完成，结果长度: {len(tool_result)} 字符\n\n"
            
            # 写入记忆
            self.messages.append({
                "role": "user",
                "content": f"Tool Result: {tool_result}"
            })
            
            # Round 2: Re-Think
            yield "data: 🧠 正在组织最终回复...\n\n"
            final_resp = await self.client.chat.completions.create(
                model="deepseek-chat",
                messages=self.messages,
                response_format={"type": "json_object"}
            )
            final_data = json.loads(final_resp.choices[0].message.content)
            
            if final_data.get("type") == "response":
                api_resp = AgentResponse(**final_data)
                # 最终回复，一个字一个字吐出来 (模拟效果，因为 DeepSeek JSON mode 不支持 stream)
                for char in api_resp.content:
                    yield f"data: {char}\n\n"
                    await asyncio.sleep(0.02)
                
                # 记忆更新
                self.messages.append({"role": "assistant", "content": api_resp.content})
            
        elif msg_type == "response":
            # ---> 直接回复分支
            api_resp = AgentResponse(**data)
            yield f"data: 🤔 {api_resp.thought}\n\n"
            for char in api_resp.content:
                yield f"data: {char}\n\n"
                await asyncio.sleep(0.02)
            self.messages.append({"role": "assistant", "content": api_resp.content})
            
        yield "data: [DONE]\n\n"

    async def _run_sync_tool(self, action: AgentAction):
        """在线程池中运行同步工具"""
        loop = asyncio.get_running_loop()
        
        if action.tool_name == "get_weather":
            # functools.partial 用于传参
            return await loop.run_in_executor(
                None, get_weather, action.args.get("city")
            )
        elif action.tool_name == "search_poi":
            return await loop.run_in_executor(
                None, lambda: search_poi(
                    action.args.get("city"),
                    action.args.get("keyword"),
                    action.args.get("poi_type")
                )
            )
        return "Unknown Tool"
