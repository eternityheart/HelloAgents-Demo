"""
Phase 6: FastAPI 后端服务 ⚡
功能: SSE 流式 API + 静态文件服务 + 行程规划 API
"""

import asyncio
import sys
import os
sys.path.append(os.getcwd())

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.phase6.api_models import ChatRequest
from src.phase6.async_agent import AsyncOrchestrator
from src.phase8.models import ItineraryRequest
from src.phase8.itinerary_generator import ItineraryGenerator
import uvicorn

app = FastAPI(title="HelloAgents API")

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局单例 Agent
agent = AsyncOrchestrator()
itinerary_gen = ItineraryGenerator()

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """智能对话接口 (流式)"""
    generator = agent.chat_generator(request.message)
    return StreamingResponse(generator, media_type="text/event-stream")

@app.post("/api/itinerary")
def create_itinerary(request: ItineraryRequest):
    """
    生成多日行程规划
    
    Args:
        destination: 目的地城市
        days: 行程天数 (1-7)
        preferences: 偏好标签列表
        start_date: 出发日期 (可选)
    
    Returns:
        结构化行程 JSON
    """
    result = itinerary_gen.generate(
        city=request.destination,
        days=request.days,
        preferences=request.preferences,
        start_date=request.start_date
    )
    return result.model_dump()

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "HelloAgents Backend is Running!"}

# 挂载静态文件 (前端页面)
# 访问 http://localhost:8000/ 即可打开前端
app.mount("/", StaticFiles(directory="src/phase7", html=True), name="frontend")

if __name__ == "__main__":
    print("🚀 HelloAgents 后端启动中...")
    print("📍 前端页面: http://127.0.0.1:8000/")
    print("📍 地图页面: http://127.0.0.1:8000/map.html")
    print("📍 行程规划: POST /api/itinerary")
    print("📍 API 文档: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)


