"""
Phase 3 核心: SimpleOrchestrator 🧠
集成了 Prompt Engineering、结构化输出、工具调用和状态管理。
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 引入我们之前写的模块
from system_prompts import get_orchestrator_prompt
from models import AgentAction, AgentResponse
from tools import get_weather, search_poi

# 设置代理
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"

load_dotenv()

class SimpleOrchestrator:
    def __init__(self):
        # 初始化 LLM 客户端
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        
        # 1. 记忆模块 (State Management)
        # 初始化时放入 System Prompt
        self.messages = [
            {"role": "system", "content": get_orchestrator_prompt()}
        ]
        
        print("🧠 SimpleOrchestrator 已启动!")

    def _call_llm(self) -> dict:
        """调用 LLM 并获取 JSON"""
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=self.messages,  # 传入完整历史记录
                response_format={"type": "json_object"},
                temperature=0.1
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"❌ LLM 调用失败: {e}")
            return {"type": "response", "content": "大脑暂时短路了...", "thought": "API Error"}

    def chat(self, user_input: str) -> str:
        """主循环：接收用户输入 -> 思考 -> (行动) -> 回复"""
        
        # 1. 将用户输入加入记忆
        self.messages.append({"role": "user", "content": user_input})
        print(f"\n👤 You: {user_input}")
        
        # 2. 思考 (Think)
        print("🧠 Thinking...", end="", flush=True)
        data = self._call_llm()
        print(" Done!")
        
        # 3. 决策 (Decide)
        msg_type = data.get("type")
        
        if msg_type == "tool_call":
            # ---> 进入工具调用流程
            return self._handle_tool_call(data)
            
        elif msg_type == "response":
            # ---> 直接回复
            response_obj = AgentResponse(**data)
            return self._handle_response(response_obj)
            
        else:
            print("⚠️ 未知消息类型，忽略")
            return "Error: Unknown message type"

    def _handle_tool_call(self, data: dict) -> str:
        """处理工具调用逻辑"""
        try:
            # 1. 解析校验
            action = AgentAction(**data)
            print(f"🤔 Thought: {action.thought}")
            print(f"🛠️ Call Tool: {action.tool_name}({action.args})")
            
            # 2. 执行工具 (Execute)
            tool_result = ""
            if action.tool_name == "get_weather":
                tool_result = get_weather(action.args.get("city"))
            elif action.tool_name == "search_poi":
                tool_result = search_poi(
                    action.args.get("city"),
                    action.args.get("keyword"),
                    action.args.get("poi_type")
                )
            else:
                tool_result = f"错误: 未找到工具 {action.tool_name}"
            
            print(f"✅ Tool Output: \n{tool_result}")
            
            # 3. 将工具结果写入记忆 (Memory Update)
            # 使用 role: user 来模拟工具返回，比 function 更通用
            self.messages.append({
                "role": "user",
                "content": f"【系统通知】工具 {action.tool_name} 执行结果:\n{tool_result}\n\n请根据上述结果回答用户问题。"
            })
            
            # 4. 再次调用 LLM 生成最终回复 (Re-Think)
            # 因为工具结果是给人看的，需要 LLM 把它转化为自然语言
            print("🧠 Synthesizing...", end="", flush=True)
            final_data = self._call_llm()
            print(" Done!")
            
            if final_data.get("type") == "response":
                final_resp = AgentResponse(**final_data)
                return self._handle_response(final_resp)
            else:
                print("⚠️ 工具执行后 LLM 没有返回 response 类型")
                return "Error: No response after tool execution"
                
        except Exception as e:
            print(f"❌ 工具执行流程出错: {e}")
            return f"Error: Tool execution failed - {e}"

    def _handle_response(self, response: AgentResponse) -> str:
        """处理直接回复"""
        print(f"🤔 Thought: {response.thought}")
        print(f"🤖 Agent: {response.content}")
        
        # 将回复加入记忆
        self.messages.append({"role": "assistant", "content": response.content})
        return response.content
