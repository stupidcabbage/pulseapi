from fastapi import APIRouter

from src.schemas.statuses import OKStatus

router = APIRouter(tags=["ping"])


@router.get("/ping")
async def ping() -> OKStatus:
    return OKStatus
