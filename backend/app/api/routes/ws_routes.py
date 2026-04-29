from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.ws_manager import manager
from app.db.deps import get_db
from app.models.booking import Booking
from app.models.class_model import Class
from sqlalchemy.orm import Session

router = APIRouter()


# 💎 helper: live stats
def get_stats(db: Session):
    total_bookings = db.query(Booking).count()
    total_classes = db.query(Class).count()

    occupancy = 0
    if total_classes > 0:
        occupancy = int((total_bookings / (total_classes * 10)) * 100)

    return {
        "total_bookings": total_bookings,
        "total_classes": total_classes,
        "occupancy_rate": occupancy
    }


@router.websocket("/ws/admin")
async def admin_ws(websocket: WebSocket):
    await manager.connect(websocket)

    db = next(get_db())

    try:
        # 🔥 initial push
        await manager.broadcast(get_stats(db))

        while True:
            # frontend ping vs ignore
            await websocket.receive_text()

            # 🔥 LIVE UPDATE
            await manager.broadcast(get_stats(db))

    except WebSocketDisconnect:
        manager.disconnect(websocket)