"""
GameMilano 后端主入口
2026米兰冬奥会应用API服务
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from . import config
from .routers import events, medals, ai, reminders
from .scripts.sync_medals import run_sync
import asyncio

# 创建FastAPI应用
app = FastAPI(
    title="GameMilano API",
    description="2026米兰-科尔蒂纳冬奥会应用后端API",
    version="1.0.0"
)

# 配置CORS，允许前端开发服务器访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(events.router)
app.include_router(medals.router)
app.include_router(ai.router)
app.include_router(reminders.router)


async def medal_sync_scheduler():
    """定时抓取奖牌榜任务"""
    while True:
        try:
            await run_sync()
        except Exception as e:
            print(f"奖牌同步后台任务出错: {e}")
        # 每 30 分钟同步一次
        await asyncio.sleep(1800)


@app.on_event("startup")
async def startup_event():
    """应用启动时启动定时任务"""
    asyncio.create_task(medal_sync_scheduler())


@app.get("/")
async def root():
    """API健康检查"""
    return {
        "status": "ok",
        "message": "GameMilano API 服务运行中",
        "version": "1.0.0"
    }


@app.get("/api/health")
async def health_check():
    """API健康检查端点"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True
    )
