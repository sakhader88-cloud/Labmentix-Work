from fastapi import APIRouter
router = APIRouter(prefix="/health", tags=["system"])

@router.get("/")
async def health_check():
    return {"status": "ok", "message": "Labmentixx backend is running"}
