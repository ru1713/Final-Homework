from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Candidate
from app.db.session import get_db

router = APIRouter()

@router.get("/graph/")
async def graph(db: AsyncSession = Depends(get_db)):
    # 研究室ノード
    lab_node = {"data": {"id": "lab", "label": "Our Lab"}}

    # DB から候補者を取得
    result = await db.execute(select(Candidate))
    candidates = result.scalars().all()

    # ノードとエッジを作る
    nodes = [lab_node] + [
        {"data": {"id": str(c.id), "label": c.full_name}} for c in candidates
    ]
    edges = [
        {"data": {"source": "lab", "target": str(c.id)}} for c in candidates
    ]

    return {"nodes": nodes, "edges": edges}