import json

import pytest

from storage import empty_week, week_from_json, week_to_json

GYM = {"name": "Gym", "days": ["Mon", "Wed"], "start": 1020, "end": 1110, "importance": 3, "malleable": True}


def test_round_trip():
    week = {"wake": 420, "activities": [GYM]}
    assert week_from_json(week_to_json(week)) == week


def test_empty_week_round_trips():
    assert week_from_json(week_to_json(empty_week())) == empty_week()


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
