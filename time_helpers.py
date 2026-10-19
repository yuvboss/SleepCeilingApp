"""Time helpers. These are yours to write (project context, section 7).

The entry screen calls the two clock conversions below to turn Streamlit's time widgets into
minutes since midnight and back. Until they're written, the entry screen shows a notice instead
of the form. The duration helper with the midnight correction belongs in this file too.
"""
import datetime


def clock_to_minutes(t: datetime.time) -> int:
    """Return t as whole minutes since midnight, 0..1439."""
    raise NotImplementedError("clock_to_minutes is not written yet")


def minutes_to_clock(m: int) -> datetime.time:
    """Return m (minutes since midnight, 0..1439) as a datetime.time."""
    raise NotImplementedError("minutes_to_clock is not written yet")
