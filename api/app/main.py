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

# ルーターを import
from .routers import health, candidate

app = FastAPI(title="Recruiting API")

# ルーターを登録
app.include_router(health.router, prefix="/health")
app.include_router(candidate.router)          # /candidates/ にマウント
