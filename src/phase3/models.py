"""
Day 3.2: Pydantic Models 结构化定义
使用 Pydantic 强类型定义 LLM 的输出结构，防止"幻觉"和格式错误。
"""

from typing import Literal, Optional, Dict, Any
from pydantic import BaseModel, Field

class AgentAction(BaseModel):
    """
    LLM 决定调用工具时的结构
    """
    type: Literal["tool_call"] = Field(description="必须是 'tool_call'")
    tool_name: str = Field(description="要调用的工具名称，如 get_weather")
    args: Dict[str, Any] = Field(description="工具参数字典")
    thought: str = Field(description="思考过程，解释为什么调用这个工具")

class AgentResponse(BaseModel):
    """
    LLM 决定直接回复时的结构
    """
    type: Literal["response"] = Field(description="必须是 'response'")
    content: str = Field(description="要回复给用户的内容")
    thought: str = Field(description="思考过程")

# 联合类型，用于解析
# 注意：在实际解析时，我们需要先判断 type 字段，再决定映射到哪个类
# 或者使用 Pydantic 的 Discriminator 功能 (这里为了教学简单，我们手动解析)
