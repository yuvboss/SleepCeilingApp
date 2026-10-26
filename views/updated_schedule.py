import streamlit as st

from recommender import recommend
from sleep_calc import SleepCalculation
from storage import DAYS, week_to_json
from time_helpers import clock_to_minutes, minutes_to_clock
from widgets import time_picker

# "Updated schedule" screen: shown when any night is red for both predicted and actual sleep.
#
# The recommender (recommender.py) is the student's: recommend(week) returns an updated COPY of the
# week with activities shortened or cut. This page shows that schedule, lets the user adjust any
# start/end time themselves, and recomputes their sleep with the student's SleepCalculation.

st.title("Updated schedule")
st.caption("Your week with activities shortened or cut to make room for sleep. You can adjust any of the times below.")

week = st.session_state.week
if any(week["wake"][day] is None for day in DAYS) or not week["activities"]:
    st.info("Enter your wake times and activities first.")
    st.page_link("views/week.py", label="Go to Enter your week")
    st.stop()


def as_hours(minutes):
    """Minutes -> text like "8h 05m"."""
    if minutes is None:
        return "—"
    if minutes < 0:
        return "Activities run past wake time"
    minutes = round(minutes)
    return f"{minutes // 60}h {minutes % 60:02d}m"


def as_clock(minutes):
    """Minutes since midnight -> a time for the pickers. Wraps past midnight, rounds to a minute."""
    return minutes_to_clock(round(minutes) % 1440)


def fresh_copy(recommended):
    return {**recommended, "activities": [dict(a) for a in recommended["activities"]]}


def clear_pickers():
    for key in [k for k in st.session_state if str(k).startswith("tweak_")]:
        del st.session_state[key]


# Run the recommender once per version of the entered week, and keep the user's edits to its result.
fingerprint = week_to_json(week)
if st.session_state.get("updated_from") != fingerprint:
    recommended = recommend(week)
    if not (isinstance(recommended, dict) and "activities" in recommended):
        st.info("The recommender doesn't return an updated week yet, so there's nothing to show here.")
        st.write(recommended)
        st.stop()
    st.session_state.recommended_week = recommended
    st.session_state.updated_week = fresh_copy(recommended)
    st.session_state.updated_from = fingerprint
    clear_pickers()

updated = st.session_state.updated_week
original_by_name = {a["name"]: a for a in week["activities"]}


def clock_text(minutes):
    """Minutes since midnight -> "9:05 PM"."""
    return as_clock(minutes).strftime("%I:%M %p").lstrip("0")


# --- Day by day: the updated schedule and the sleep it leaves ---
# Each row is one day: that day's activities with their new times, and the sleep that night
# (from the end of that evening to the next morning's wake time).
before = SleepCalculation(week)
after = SleepCalculation(updated)
kept_names = {a["name"] for a in updated["activities"]}

table = st.container(border=True)
def activity_line(a):
    """ "Homework: 7:52 PM – 9:07 PM  (was 8:30 PM – 11:00 PM)" — the old times only when they changed."""
    line = f"{a['name']}: {clock_text(a['start'])} – {clock_text(a['end'])}"
    original = original_by_name.get(a["name"])
    if original and (round(a["start"]) % 1440, round(a["end"]) % 1440) != (original["start"], original["end"]):
        line += f"  :gray[(was {clock_text(original['start'])} – {clock_text(original['end'])})]"
    return line


day_col, schedule_col, sleep_col = table.columns([1, 3, 2])
day_col.markdown("**Day**")
schedule_col.markdown("**Updated schedule**")
sleep_col.markdown("**New sleep time**")
for i, day in enumerate(DAYS):
    table.divider()
    day_col, schedule_col, sleep_col = table.columns([1, 3, 2])
    day_col.markdown(f"**{day}**")

    lines = [
        activity_line(a)
        for a in sorted(updated["activities"], key=lambda a: a["start"])
        if day in a["days"]
    ]
    lines += [
        f":red[~~{a['name']}: {clock_text(a['start'])} – {clock_text(a['end'])}~~ cut]"
        for a in week["activities"]
        if day in a["days"] and a["name"] not in kept_names
    ]
    schedule_col.markdown("  \n".join(lines) if lines else "Nothing scheduled")

    night = (i + 1) % 7  # the night after this day ends on the next morning
    change = ""
    if before[night] is not None and after[night] is not None and round(after[night] - before[night]) != 0:
        change = f"  \n({round(after[night] - before[night]):+d} min)"
    sleep_col.markdown(f"**{as_hours(after[night])}**" + change)

st.caption("New sleep time is the sleep that night, until the next morning's wake-up time.")


# --- Adjust the times ---
st.subheader(":material/tune: Adjust the times")
st.caption("These are the recommended times. Change any of them and the schedule above updates.")


def save_tweak(index, field):
    t = st.session_state[f"tweak_{field}_{index}"]
    if t is not None:
        updated["activities"][index][field] = clock_to_minutes(t)


for i, activity in enumerate(updated["activities"]):
    original = original_by_name.get(activity["name"])
    name_col, start_col, end_col = st.columns([2, 1, 1])
    label = f"**{activity['name']}** · {', '.join(activity['days'])}"
    if original:
        length_before = (original["end"] - original["start"]) % 1440
        length_now = round(activity["end"] - activity["start"]) % 1440
        if length_now == 0 and length_before != 0:
            label += "  \n:red[cut]"
        elif length_now != length_before:
            label += f"  \n{length_before} → {length_now} min"
    name_col.markdown(label)
    time_picker(
        "Start", value=as_clock(activity["start"]), key=f"tweak_start_{i}",
        on_change=save_tweak, args=(i, "start"), container=start_col, every_minute=True,
    )
    time_picker(
        "End", value=as_clock(activity["end"]), key=f"tweak_end_{i}",
        on_change=save_tweak, args=(i, "end"), container=end_col, every_minute=True,
    )


kept = {a["name"] for a in updated["activities"]}
for activity in week["activities"]:
    if activity["name"] not in kept:
        st.markdown(f"**{activity['name']}** · {', '.join(activity['days'])}  \n:red[cut]")


def reset():
    st.session_state.updated_week = fresh_copy(st.session_state.recommended_week)
    clear_pickers()


st.button("Reset to the recommendation", on_click=reset, icon=":material/restart_alt:")
