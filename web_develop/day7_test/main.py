"""个人记账 FastAPI：项目入口。"""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import create_db_and_tables
from routers.auth import router as auth_router
from routers.transactions import router as transactions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI 启动时初始化数据库。"""
    create_db_and_tables()
    yield


app = FastAPI(
    title="Personal Finance API",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(transactions_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
