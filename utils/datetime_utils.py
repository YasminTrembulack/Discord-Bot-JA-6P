# utils/datetime_utils.py
from datetime import datetime, timedelta

def generate_next_days(start: datetime, max_days: int, allowed_weekdays: set, holidays: set):
    days = []
    delta = 1
    while len(days) < max_days:
        day = start + timedelta(days=delta)
        if day.weekday() in allowed_weekdays and day.date() not in holidays:
            days.append(day.strftime("%d/%m/%Y"))
        delta += 1
    return days

def generate_time_slots(start_time: datetime, end_time: datetime, interval: int):
    slots = []
    current = start_time
    while current < end_time:
        slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=interval)
    return slots

def get_available_time_slots(start_time: datetime, end_time: datetime, interval: int, unavailable_time_slots: list) -> list:
    available = []
    current = start_time
    while current < end_time:
        time_str = current.strftime("%H:%M")
        if time_str not in unavailable_time_slots:
            available.append(time_str)
        current += timedelta(minutes=interval)
    return available

def generate_possible_end_times(current: datetime, blocks: int, unavailable_time_slots: list, interval: int, end_time: datetime) -> list:
    possible_ends = []
    while True:
        current += timedelta(minutes=interval)
        time_str = current.strftime("%H:%M")
        if time_str in unavailable_time_slots or current >= end_time:
            possible_ends.append(time_str)
            break
        possible_ends.append(time_str)
        if blocks >= 1:
            blocks -= 1
            if blocks == 0:
                break
    return possible_ends