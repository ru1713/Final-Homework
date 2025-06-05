from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Recruiting API")

# --- ここを追加 ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------

from .routers import health, candidate
app.include_router(health.router, prefix="/health")
app.include_router(candidate.router)          # /candidates/ にマウント

# すでに health, candidate を登録している場所に ↓ を追加
from .routers import graph
app.include_router(graph.router)
