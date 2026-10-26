"""A time picker that shows 12-hour times ("9:05 PM").

Streamlit's own st.time_input only shows 24-hour times, so this is a searchable dropdown instead.
It returns a datetime.time (or None while empty), exactly like st.time_input, so the code that uses
it converts with clock_to_minutes as before.
"""
import datetime

import streamlit as st

EVERY_5_MINUTES = [datetime.time(m // 60, m % 60) for m in range(0, 1440, 5)]
EVERY_MINUTE = [datetime.time(m // 60, m % 60) for m in range(1440)]


def twelve_hour(t):
    return t.strftime("%I:%M %p").lstrip("0")


def time_picker(label, value=None, key=None, on_change=None, args=None, container=st,
                label_visibility="visible"):
    """Like st.time_input(label, value=..., key=..., on_change=..., args=...), in AM/PM.

    `value` is a datetime.time or None. Times are offered every 5 minutes, or every minute when the
    current value isn't on a 5-minute mark (e.g. a time the recommender worked out).
    """
    on_grid = value is None or value.minute % 5 == 0
    options = EVERY_5_MINUTES if on_grid else EVERY_MINUTE
    return container.selectbox(
        label,
        options,
        index=None if value is None else options.index(value.replace(second=0, microsecond=0)),
        format_func=twelve_hour,
        placeholder="Choose a time",
        key=key,
        on_change=on_change,
        args=args,
        label_visibility=label_visibility,
    )
