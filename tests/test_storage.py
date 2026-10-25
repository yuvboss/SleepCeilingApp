import json

import pytest

from storage import DAYS, empty_week, week_from_json, week_to_json

GYM = {"name": "Gym", "days": ["Mon", "Wed"], "start": 1020, "end": 1110, "importance": 3, "malleable": True}
WAKE = {"Mon": 400, "Tue": 400, "Wed": 400, "Thu": 400, "Fri": 400, "Sat": 660, "Sun": 660}


def test_round_trip():
    week = {"wake": WAKE, "wake_default": 400, "activities": [GYM]}
    assert week_from_json(week_to_json(week)) == week


def test_empty_week_round_trips():
    assert week_from_json(week_to_json(empty_week())) == empty_week()


def test_file_from_before_per_day_wake_times_still_loads():
    loaded = week_from_json(json.dumps({"wake": 420, "activities": [GYM]}))
    assert loaded["wake"] == {day: 420 for day in DAYS}
    assert loaded["wake_default"] == 420


@pytest.mark.parametrize(
    "wake",
    [
        {"Mon": 400},  # missing days
        dict(WAKE, Sat=1440),  # out of range
        dict(WAKE, Sun="11:00"),  # not minutes
    ],
)
def test_bad_wake_times_are_rejected(wake):
    with pytest.raises(ValueError):
        week_from_json(json.dumps({"wake": wake, "wake_default": 400, "activities": []}))


def test_days_come_back_in_week_order_without_duplicates():
    late = dict(GYM, days=["Fri", "Mon", "Fri"])
    loaded = week_from_json(json.dumps({"wake": None, "activities": [late]}))
    assert loaded["activities"][0]["days"] == ["Mon", "Fri"]


def test_midnight_crossing_activity_is_accepted():
    shift = dict(GYM, start=1320, end=30)
    assert week_from_json(json.dumps({"wake": 420, "activities": [shift]}))["activities"][0]["end"] == 30


@pytest.mark.parametrize(
    "bad",
    [
        {"name": ""},
        {"days": []},
        {"days": ["Monday"]},
        {"start": 1440},
        {"end": -1},
        {"start": 60.5},
        {"importance": 0},
        {"importance": 6},
        {"importance": True},
        {"malleable": "yes"},
    ],
)
def test_bad_activity_is_rejected(bad):
    with pytest.raises(ValueError):
        week_from_json(json.dumps({"wake": 420, "activities": [dict(GYM, **bad)]}))


@pytest.mark.parametrize("text", ["not json", "[]", '{"wake": 420}', '{"wake": 2000, "activities": []}'])
def test_bad_file_is_rejected(text):
    with pytest.raises(ValueError):
        week_from_json(text)
