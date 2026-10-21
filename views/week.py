# Screen 2 — Enter your week. This is where the week in st.session_state.week gets filled in:
# the wake time, then activities added/edited through a pop-up (the "modal" in the project context).
# It converts what the widgets give (datetime.time) into integer minutes using YOUR helpers in
# time_helpers.py, so every number stored in the week is minutes since midnight.
import datetime

import streamlit as st

from storage import DAYS
from time_helpers import clock_to_minutes, minutes_to_clock

DAY_NAMES = dict(zip(DAYS, ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]))

# A shortcut to the shared week. Changing `week` here changes st.session_state.week.
week = st.session_state.week

st.title("Enter your week")

# Until both clock conversions are written, show a notice instead of a form that can't save.
try:
    clock_to_minutes(datetime.time(0, 0))
    minutes_to_clock(0)
except NotImplementedError:
    st.warning(
        "The clock conversions in `time_helpers.py` aren't written yet, so times can't be saved. "
        "This screen will work once `clock_to_minutes` and `minutes_to_clock` are done."
    )
    st.stop()


def clock(m):
    """Minutes since midnight -> "9:05 PM" style text for showing on screen."""
    return minutes_to_clock(m).strftime("%I:%M %p").lstrip("0")


# --- Wake time: set once, applies to every night ---

def save_wake():
    """Runs when the wake-time picker changes: stores it in week["wake"] as minutes."""
    t = st.session_state.wake_input
    week["wake"] = None if t is None else clock_to_minutes(t)


st.time_input(
    "Wake-up time (the same every day)",
    value=None if week["wake"] is None else minutes_to_clock(week["wake"]),
    step=300,
    key="wake_input",
    on_change=save_wake,
)


# --- Activity modal: adds a new activity, or edits / deletes an existing one ---

@st.dialog("Activity")
def activity_dialog(index=None):
    """The pop-up form. index=None adds a new activity; a number edits week["activities"][index]."""
    existing = week["activities"][index] if index is not None else None

    name = st.text_input("Activity name", value=existing["name"] if existing else "")
    days = st.multiselect(
        "Days", DAYS, default=existing["days"] if existing else [], format_func=DAY_NAMES.get
    )
    left, right = st.columns(2)
    start = left.time_input(
        "Start", value=minutes_to_clock(existing["start"]) if existing else None, step=300
    )
    end = right.time_input(
        "End", value=minutes_to_clock(existing["end"]) if existing else None, step=300
    )
    st.caption("An end time earlier than the start means it runs past midnight.")
    importance = st.slider(
        "Importance",
        1,
        5,
        value=existing["importance"] if existing else 3,
        help="5 = untouchable, 1 = fully expendable.",
    )
    malleable = st.checkbox(
        "Could be moved to a different time in the week",
        value=existing["malleable"] if existing else False,
    )

    save_col, delete_col = st.columns(2)
    if save_col.button("Save", type="primary"):
        problems = []
        if not name.strip():
            problems.append("Give it a name.")
        if not days:
            problems.append("Pick at least one day.")
        if start is None or end is None:
            problems.append("Set a start and an end time.")
        elif start == end:
            problems.append("Start and end can't be the same time.")
        if problems:
            for p in problems:
                st.error(p)
            return
        # THIS is where an activity is created: exactly the dictionary your calculation reads.
        activity = {
            "name": name.strip(),
            "days": [d for d in DAYS if d in days],
            "start": clock_to_minutes(start),
            "end": clock_to_minutes(end),
            "importance": importance,
            "malleable": malleable,
        }
        if existing:
            week["activities"][index] = activity
        else:
            week["activities"].append(activity)
        st.rerun()

    if existing and delete_col.button("Delete"):
        del week["activities"][index]
        st.rerun()


# --- The grid: Days | Activities, Monday to Sunday ---
# Each activity is stored once but shown under every day in its "days" list, sorted by start time.
# Clicking one opens the pop-up to edit it.

st.subheader("Activities")
if st.button("Add activity"):
    activity_dialog()

header_day, header_acts = st.columns([1, 3])
header_day.markdown("**Days**")
header_acts.markdown("**Activities**")

for day in DAYS:
    day_col, acts_col = st.columns([1, 3])
    day_col.write(DAY_NAMES[day])
    on_day = [i for i, a in enumerate(week["activities"]) if day in a["days"]]
    on_day.sort(key=lambda i: week["activities"][i]["start"])
    if not on_day:
        acts_col.caption("Nothing yet")
    for i in on_day:
        a = week["activities"][i]
        label = f"{a['name']}  ·  {clock(a['start'])}–{clock(a['end'])}"
        if acts_col.button(label, key=f"activity-{day}-{i}"):
            activity_dialog(i)
