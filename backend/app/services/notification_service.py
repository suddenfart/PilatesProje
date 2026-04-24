from datetime import datetime, timedelta
from fastapi import BackgroundTasks


# -------------------------
# SIMPLE IN-MEMORY NOTIFIER
# (prod'da Redis + Celery olur)
# -------------------------

active_connections = []


def add_connection(websocket):
    active_connections.append(websocket)


def remove_connection(websocket):
    active_connections.remove(websocket)


async def broadcast(message: dict):
    for connection in active_connections:
        await connection.send_json(message)


# -------------------------
# BOOKING NOTIFICATION
# -------------------------
async def send_booking_notification(user_id: int, class_time: datetime):
    await broadcast({
        "type": "booking_confirmed",
        "user_id": user_id,
        "message": f"Booking confirmed for {class_time}"
    })


# -------------------------
# REMINDER LOGIC
# -------------------------
def schedule_reminder(background_tasks: BackgroundTasks, user_id: int, class_time: datetime):

    reminder_time = class_time - timedelta(hours=1)

    background_tasks.add_task(
        delayed_reminder,
        user_id,
        class_time,
        reminder_time
    )


async def delayed_reminder(user_id: int, class_time: datetime, reminder_time: datetime):

    now = datetime.utcnow()

    wait_seconds = (reminder_time - now).total_seconds()

    if wait_seconds > 0:
        import asyncio
        await asyncio.sleep(wait_seconds)

    await broadcast({
        "type": "class_reminder",
        "user_id": user_id,
        "message": f"Your class starts at {class_time}"
    })