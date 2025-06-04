from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.db.session import get_db
from app.db import models
from app.schemas import (
    CandidateCreate,
    CandidateUpdate,
    CandidateOut,
)

router = APIRouter(prefix="/candidates", tags=["candidates"])

# ───────────────────────────────────────────
# Create  ─ POST /candidates/
# ───────────────────────────────────────────
@router.post(
    "/",
    response_model=CandidateOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_candidate(
    payload: CandidateCreate,
    db: AsyncSession = Depends(get_db),
):
    obj = models.Candidate(**payload.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


# ───────────────────────────────────────────
# Read (list) ─ GET /candidates/
# ───────────────────────────────────────────
@router.get("/", response_model=list[CandidateOut])
async def list_candidates(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(models.Candidate))
    return res.scalars().all()


# ───────────────────────────────────────────
# Read (single) ─ GET /candidates/{id}
# ───────────────────────────────────────────
@router.get("/{candidate_id}", response_model=CandidateOut)
async def get_candidate(candidate_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(models.Candidate, candidate_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return obj


# ───────────────────────────────────────────
# Update ─ PUT /candidates/{id}
# ───────────────────────────────────────────
@router.put("/{candidate_id}", response_model=CandidateOut)
async def update_candidate(
    candidate_id: int,
    payload: CandidateUpdate,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        update(models.Candidate)
        .where(models.Candidate.id == candidate_id)
        .values(**payload.dict(exclude_unset=True))
        .returning(models.Candidate)
    )
    res = await db.execute(stmt)
    await db.commit()
    obj = res.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return obj


# ───────────────────────────────────────────
# Delete ─ DELETE /candidates/{id}
# ───────────────────────────────────────────
@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(
    candidate_id: int,
    db: AsyncSession = Depends(get_db),
):
    res = await db.execute(
        delete(models.Candidate).where(models.Candidate.id == candidate_id)
    )
    await db.commit()
    if res.rowcount == 0:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return