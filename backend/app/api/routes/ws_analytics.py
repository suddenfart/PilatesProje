from fastapi import APIRouter, WebSocket
from app.services.ws_manager import manager

router = APIRouter()


@router.websocket("/ws/admin")
async def admin_ws(websocket: WebSocket):

    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()  # keep alive

    except Exception:
        manager.disconnect(websocket)