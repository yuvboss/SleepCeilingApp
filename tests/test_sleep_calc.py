from sleep_calc import SleepCalculation
from storage import DAYS


def activity(name, days, start, end, importance=3):
    return {"name": name, "days": days, "start": start, "end": end, "importance": importance, "malleable": False}


def same_wake(minutes):
    return {day: minutes for day in DAYS}


def test_project_context_section_4_check():
    # Sunday homework 19:00-23:00, Monday practice 15:30-17:30, Monday wake 06:40.
    # Monday must be 460; 790 would mean the days are off by one.
    week = {
        "wake": same_wake(400),
        "activities": [
            activity("Homework", ["Sun"], 1140, 1380),
            activity("Practice", ["Mon"], 930, 1050),
        ],
    }
    nights = SleepCalculation(week)
    assert nights[0] == 460
    assert nights[1] == 790


def test_project_context_friday_example():
    # Friday's last activity ends 01:30 Saturday, Saturday wake 11:00: Saturday's night is 570.
    wake = dict(same_wake(400), Sat=660)
    week = {"wake": wake, "activities": [activity("Party", ["Fri"], 1200, 90)]}
    assert SleepCalculation(week)[DAYS.index("Sat")] == 570


def test_practice_week_with_weekend_lie_in():
    wake = dict(same_wake(420), Sat=600, Sun=600)
    week = {
        "wake": wake,
        "activities": [
            activity("School", ["Mon", "Tue", "Wed", "Thu", "Fri"], 480, 900, 5),
            activity("Homework", ["Mon", "Tue"], 1260, 1380),
            activity("Shift", ["Fri"], 1320, 30, 4),
        ],
    }
    assert SleepCalculation(week) == [None, 480, 480, 960, 960, 570, None]


def test_returns_seven_nights_in_morning_order():
    week = {"wake": same_wake(420), "activities": [activity("Club", DAYS, 1200, 1260)]}
    assert SleepCalculation(week) == [600] * 7


def test_overlapping_activities_are_not_double_counted():
    week = {
        "wake": same_wake(420),
        "activities": [
            activity("Practice", ["Mon"], 960, 1200),
            activity("Homework", ["Mon"], 1140, 1320),  # overlaps practice
        ],
    }
    assert SleepCalculation(week)[DAYS.index("Tue")] == 540


def test_night_running_past_wake_time_stays_negative():
    # Section 4: a week that can't happen as entered is surfaced, not clamped to zero.
    week = {"wake": same_wake(420), "activities": [activity("Shift", ["Mon"], 1380, 480)]}
    assert SleepCalculation(week)[DAYS.index("Tue")] == -60


def test_empty_week_has_no_nights():
    assert SleepCalculation({"wake": same_wake(420), "activities": []}) == [None] * 7


def test_does_not_change_the_week_it_is_given():
    week = {"wake": same_wake(420), "activities": [activity("Club", ["Mon"], 1200, 1260)]}
    before = repr(week)
    SleepCalculation(week)
    assert repr(week) == before
