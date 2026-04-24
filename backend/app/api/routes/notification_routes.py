from fastapi import APIRouter, WebSocket
from app.services.notification_service import add_connection, remove_connection

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    add_connection(websocket)

    try:
        while True:
            await websocket.receive_text()

    except Exception:
        remove_connection(websocket)