from datetime import datetime, timedelta
from app.models.class_model import Class
from app.services.studio_engine import (
    is_overlapping,
    is_holiday
)


def generate_weekly_slots(
    start_date: datetime,
    days: int,
    start_hour: int,
    end_hour: int,
    duration_minutes: int
):

    slots = []
    current_day = start_date

    for _ in range(days):

        # 🚫 HOLIDAY SKIP
        if is_holiday(current_day):
            current_day += timedelta(days=1)
            continue

        day_start = current_day.replace(
            hour=start_hour,
            minute=0,
            second=0,
            microsecond=0
        )

        day_end = current_day.replace(
            hour=end_hour,
            minute=0,
            second=0,
            microsecond=0
        )

        slot_time = day_start

        while slot_time + timedelta(minutes=duration_minutes) <= day_end:

            slots.append({
                "start_time": slot_time,
                "end_time": slot_time + timedelta(minutes=duration_minutes)
            })

            slot_time += timedelta(minutes=duration_minutes)

        current_day += timedelta(days=1)

    return slots