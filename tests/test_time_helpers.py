import datetime

import pytest

from time_helpers import clock_to_minutes, duration, minutes_to_clock


@pytest.mark.parametrize(
    "hour, minute, expected",
    [(0, 0, 0), (7, 0, 420), (12, 0, 720), (19, 30, 1170), (23, 59, 1439)],
)
def test_clock_to_minutes(hour, minute, expected):
    assert clock_to_minutes(datetime.time(hour, minute)) == expected


@pytest.mark.parametrize(
    "m, hour, minute",
    [(0, 0, 0), (420, 7, 0), (720, 12, 0), (1170, 19, 30), (1439, 23, 59)],
)
def test_minutes_to_clock(m, hour, minute):
    assert minutes_to_clock(m) == datetime.time(hour, minute)


def test_conversions_undo_each_other_for_every_minute_of_the_day():
    for m in range(1440):
        assert clock_to_minutes(minutes_to_clock(m)) == m


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1260, 1380, 120),  # 21:00-23:00, same day
        (480, 900, 420),  # 8:00-15:00, school day
        (1320, 30, 150),  # 22:00-00:30, crosses midnight
        (1380, 60, 120),  # 23:00-01:00, crosses midnight
        (1439, 0, 1),  # 23:59-00:00, one minute across midnight
        (0, 1439, 1439),  # the whole day but one minute
        (600, 600, 0),  # zero length, e.g. shortened to a floor of 0
    ],
)
def test_duration(start, end, expected):
    assert duration(start, end) == expected
