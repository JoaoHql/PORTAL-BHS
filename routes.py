from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Servidor de chat operacional"}

@router.get("/status")
async def status():
    return {
        "service": "chat-backend",
        "version": "1.0.0",
        "websocket_active": True,
        "llm_ready": True
    }