"""
Phase 6: API Data Models 📦
定义请求和响应的 Pydantic 模型。
"""

from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"
    city: str = "北京"  # 模拟前端定位上下文

class ChatResponse(BaseModel):
    # 这里定义非流式返回的结构 (如果需要的话)
    status: str
    content: str
