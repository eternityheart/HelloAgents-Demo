"""
Phase 6: FastAPI 后端服务 ⚡
功能: SSE 流式 API + 静态文件服务
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

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """智能对话接口 (流式)"""
    generator = agent.chat_generator(request.message)
    return StreamingResponse(generator, media_type="text/event-stream")

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
    print("📍 API 文档: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)

