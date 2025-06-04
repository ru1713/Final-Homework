from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["health"])
def ping():
    return {"status": "ok"}
