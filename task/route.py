from fastapi import APIRouter

router = APIRouter(prefix="/task", tags=["task"])

@router.post('')
async def task():
    return {"task": "task"}