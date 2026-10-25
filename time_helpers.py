"""Time helpers. These are yours to write (project context, section 7).

The entry screen calls the two clock conversions below to turn Streamlit's time widgets into
minutes since midnight and back. Until they're written, the entry screen shows a notice instead
of the form. The duration helper with the midnight correction belongs in this file too.
"""
import datetime


def clock_to_minutes(t: datetime.time) -> int:
    return t.hour*60 + t.minute


def minutes_to_clock(m: int) -> datetime.time:
    return datetime.time(m//60,m%60)

def duration(start,end):
    if end>=start:
        return end - start 
    elif start>end:
        return ((24*60)+end)-start
