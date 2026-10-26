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
                label_visibility="visible", every_minute=False):
    """Like st.time_input(label, value=..., key=..., on_change=..., args=...), in AM/PM.

    `value` is a datetime.time or None. Times are offered every 5 minutes, or every minute with
    every_minute=True (for times the recommender works out, like 5:52 PM). A picker must always use
    the same list: switching lists makes Streamlit reset it to the first entry.
    """
    options = EVERY_MINUTE if every_minute else EVERY_5_MINUTES
    if value is not None:
        value = value.replace(second=0, microsecond=0)
        if value not in options:  # e.g. 5:52 PM in a 5-minute list: show the nearest 5 minutes
            minutes = round((value.hour * 60 + value.minute) / 5) * 5 % 1440
            value = datetime.time(minutes // 60, minutes % 60)
    if key is not None:
        # Push the value into the widget's own state. Changing only the default isn't enough: the
        # browser keeps showing the old choice (e.g. blank) unless the widget's state changes.
        if st.session_state.get(key, "unset") != value:
            st.session_state[key] = value
        index = 0  # the shown value comes from session state
    else:
        index = None if value is None else options.index(value)
    return container.selectbox(
        label,
        options,
        index=index,
        format_func=twelve_hour,
        placeholder="Choose a time",
        key=key,
        on_change=on_change,
        args=args,
        label_visibility=label_visibility,
    )
