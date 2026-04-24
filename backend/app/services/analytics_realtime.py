from app.services.ws_manager import manager
from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.models.class_model import Class
from sqlalchemy import func


async def send_live_update(db: Session):

    total_bookings = db.query(Booking).count()

    total_classes = db.query(Class).count()

    total_capacity = db.query(Class).with_entities(
        func.sum(Class.capacity)
    ).scalar() or 0

    occupancy = 0
    if total_capacity:
        occupancy = (total_bookings / total_capacity) * 100

    payload = {
        "type": "analytics_update",
        "data": {
            "total_bookings": total_bookings,
            "total_classes": total_classes,
            "occupancy_rate": round(occupancy, 2)
        }
    }

    await manager.broadcast(payload)