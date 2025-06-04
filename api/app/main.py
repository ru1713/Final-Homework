from fastapi import FastAPI

# ルーターを import
from .routers import health, candidate

app = FastAPI(title="Recruiting API")

# ルーターを登録
app.include_router(health.router, prefix="/health")
app.include_router(candidate.router)          # /candidates/ にマウント
