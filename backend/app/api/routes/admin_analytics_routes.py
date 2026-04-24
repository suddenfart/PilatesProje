from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.db.deps import get_db
from app.models.booking import Booking
from app.models.class_model import Class
from app.models.user_package import UserPackage

router = APIRouter()


# -------------------------
# OVERALL DASHBOARD METRICS
# -------------------------
@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):

    total_classes = db.query(Class).count()
    total_bookings = db.query(Booking).count()
    total_users = db.query(UserPackage.user_id).distinct().count()

    total_capacity = db.query(Class).with_entities(
        func.sum(Class.capacity)
    ).scalar() or 0

    occupancy_rate = 0
    if total_capacity > 0:
        occupancy_rate = (total_bookings / total_capacity) * 100

    return {
        "total_classes": total_classes,
        "total_bookings": total_bookings,
        "total_users": total_users,
        "occupancy_rate": round(occupancy_rate, 2)
    }


# -------------------------
# REVENUE (SESSION-BASED)
# -------------------------
@router.get("/revenue")
def revenue(db: Session = Depends(get_db)):

    packages = db.query(UserPackage).all()

    total_sessions_sold = sum(p.total_sessions for p in packages)
    total_remaining = sum(p.remaining_sessions for p in packages)

    return {
        "total_sessions_sold": total_sessions_sold,
        "remaining_sessions": total_remaining,
        "used_sessions": total_sessions_sold - total_remaining
    }


# -------------------------
# PEAK HOURS ANALYSIS
# -------------------------
@router.get("/peak-hours")
def peak_hours(db: Session = Depends(get_db)):

    results = db.query(
        func.extract('hour', Class.start_time).label("hour"),
        func.count(Booking.id)
    ).join(Booking, Booking.class_id == Class.id)\
     .group_by("hour")\
     .order_by(func.count(Booking.id).desc())\
     .all()

    return [
        {
            "hour": int(r[0]),
            "bookings": r[1]
        }
        for r in results
    ]


# -------------------------
# DAILY BOOKINGS TREND
# -------------------------
@router.get("/bookings/daily")
def daily_bookings(db: Session = Depends(get_db)):

    results = db.query(
        func.date(Booking.id).label("date"),
        func.count(Booking.id)
    ).group_by("date").all()

    return [
        {
            "date": str(r[0]),
            "bookings": r[1]
        }
        for r in results
    ]


# -------------------------
# PACKAGE HEALTH
# -------------------------
@router.get("/packages")
def package_health(db: Session = Depends(get_db)):

    packages = db.query(UserPackage).all()

    active = 0
    empty = 0

    for p in packages:
        if p.remaining_sessions > 0:
            active += 1
        else:
            empty += 1

    return {
        "total_users": len(packages),
        "active_packages": active,
        "empty_packages": empty
    }


# -------------------------
# LIVE SNAPSHOT (REAL-TIME KPI)
# -------------------------
@router.get("/live")
def live_snapshot(db: Session = Depends(get_db)):

    now = datetime.utcnow()

    today_bookings = db.query(Booking).filter(
        func.date(Booking.id) == now.date()
    ).count()

    return {
        "timestamp": now,
        "today_bookings": today_bookings
    }