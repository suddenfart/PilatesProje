from datetime import datetime, timedelta
from app.models.class_model import Class
from app.models.booking import Booking


# -----------------------------
# OVERLAP CHECK
# -----------------------------
def is_overlapping(db, start_time, end_time):
    return db.query(Class).filter(
        Class.start_time < end_time,
        Class.end_time > start_time
    ).first()


# -----------------------------
# CAPACITY CHECK
# -----------------------------
def is_full(db, class_id):
    count = db.query(Booking).filter(
        Booking.class_id == class_id
    ).count()

    return count >= 6


# -----------------------------
# HOLIDAY SKIP SYSTEM
# -----------------------------
def is_holiday(date: datetime):
    # basit örnek (sonra DB'ye bağlanabilir)
    holidays = [
        "2026-01-01",
        "2026-04-23"
    ]

    return date.strftime("%Y-%m-%d") in holidays


# -----------------------------
# INSTRUCTOR CONFLICT CHECK
# -----------------------------
def instructor_conflict(db, instructor_id, start_time, end_time):
    return db.query(Class).filter(
        Class.instructor_id == instructor_id,
        Class.start_time < end_time,
        Class.end_time > start_time
    ).first()