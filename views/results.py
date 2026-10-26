import streamlit as st
from sleep_calc import SleepCalculation
from storage import DAYS 
from time_helpers import minutes_to_clock
from flow import send_back_to_week, go_to_good_job, go_to_updated_schedule
from diagnosis import Conditions

st.title("Results")
week = st.session_state.week
track = 0
for day in DAYS:
    if week["wake"][day] == None:
        track += 1
if track > 0:
    st.warning("Add wake times before getting results")
    st.page_link("views/week.py", label="Go to Enter your week") 
    st.stop()
if week["activities"] == []:
    st.warning("Add activities before getting results")
    st.page_link("views/week.py", label="Go to Enter your week") 
    st.stop()
PredictedSleep = SleepCalculation(week)

#st.write(PredictedSleep)
day, predicted, real = st.columns(3)
#Headers
day.markdown("**Day**")
predicted.markdown("**Sleep Ceiling**")
real.markdown("**Real Sleep**")
def as_hours(minutes):
    """Predicted minutes -> text like "8h 05m" for the table. The numbers themselves stay in minutes."""
    if minutes is None:
        return "—"
    if minutes < 0:
        return "Activities run past wake time"
    return f"{minutes // 60}h {minutes % 60:02d}m"


#Rows
# ActualSleep collects what the user types for each night, in hours (e.g. 7h 30m -> 7.5), Mon..Sun.
# The user types hours and minutes in two boxes; a night with both boxes empty is None.
ActualSleep = []
for i, row in enumerate(DAYS):
    day, predicted, real = st.columns(3)
    day.write(row)
    if PredictedSleep[i] == None:
        predicted.markdown(f":yellow[{as_hours(PredictedSleep[i])}]")
    elif PredictedSleep[i] >= 510:
        predicted.markdown(f":green[{as_hours(PredictedSleep[i])}]")
    else:
        predicted.markdown(f":red[{as_hours(PredictedSleep[i])}]")
    hours_box, minutes_box = real.columns(2)
    hours = hours_box.number_input(
        f"Hours slept on {row} night", key=f"actual_h_{row}", min_value=0, max_value=24, step=1,
        value=None, placeholder="h", label_visibility="collapsed",
    )
    minutes = minutes_box.number_input(
        f"Minutes slept on {row} night", key=f"actual_m_{row}", min_value=0, max_value=55, step=5,
        value=None, placeholder="min", label_visibility="collapsed",
    )
    actual = None if hours is None and minutes is None else (hours or 0) + (minutes or 0) / 60
    ActualSleep.append(actual)
    if actual == None:
        real.markdown(f":yellow[{actual}]")
    elif actual*60 >=510:
        real.markdown(f":green[{as_hours(round(actual * 60))}]")
    elif actual*60 < 510:
        real.markdown(f":red[{as_hours(round(actual * 60))}]")


# --- Proceed: once the actual sleep is filled in, send the user to the next screen ---
if st.button("Proceed", type="primary"):
    Conditions(PredictedSleep, ActualSleep)
    