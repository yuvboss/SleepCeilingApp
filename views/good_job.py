import streamlit as st

from sleep_calc import SleepCalculation
from storage import DAYS

# "Good job" screen: shown when every night is green for both predicted and actual sleep.
# Project context, section 2: say so plainly. No invented problems, no optimisation tips, no badges.

week = st.session_state.week
if any(week["wake"][day] is None for day in DAYS) or not week["activities"]:
    st.info("Enter your wake times and activities first.")
    st.page_link("views/week.py", label="Go to Enter your week")
    st.stop()


def as_hours(minutes):
    """Minutes -> text like "8h 05m"."""
    if minutes is None or minutes < 0:
        return "—"
    minutes = round(minutes)
    return f"{minutes // 60}h {minutes % 60:02d}m"


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;700&display=swap');
    .done-sky {
        position: relative;
        text-align: center;
        padding: 2.5rem 1rem 2rem;
        border-radius: 1.25rem;
        background: radial-gradient(circle at 50% 0%, #2B3A8C 0%, #161D45 55%, #0E1326 100%);
        overflow: hidden;
    }
    .done-sky .star { position: absolute; width: 3px; height: 3px; border-radius: 50%; background: #E6E9F5; opacity: 0.7; }
    .done-moon { font-size: 4.5rem; line-height: 1; filter: drop-shadow(0 0 18px rgba(255, 233, 170, 0.45)); }
    div.done-title {
        font-family: 'Fredoka', sans-serif !important;
        font-weight: 700 !important;
        font-size: clamp(2rem, 6vw, 3rem) !important;
        margin-top: 0.75rem;
        color: #E6E9F5;
    }
    div.done-text { font-size: 1.1rem !important; opacity: 0.8; margin-top: 0.5rem; color: #E6E9F5; }
    </style>
    <div class="done-sky">
        <span class="star" style="top:18%; left:12%"></span>
        <span class="star" style="top:30%; left:24%"></span>
        <span class="star" style="top:14%; left:70%"></span>
        <span class="star" style="top:40%; left:84%"></span>
        <span class="star" style="top:62%; left:8%"></span>
        <span class="star" style="top:70%; left:91%"></span>
        <span class="star" style="top:24%; left:46%"></span>
        <div class="done-moon">🌙</div>
        <div class="done-title">Your week works</div>
        <div class="done-text">Each night gives you room for 8h and 30min of sleep or more, and you are getting it!</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
st.subheader("Your sleep this week")
nights = SleepCalculation(week)
for column, day, night in zip(st.columns(7), DAYS, nights):
    with column.container(border=True):
        st.caption(day)
        st.markdown(f"**{as_hours(night)}**")
st.caption("Predicted sleep each night, by the morning it ends on.")

st.write("")
left, right = st.columns(2)
left.page_link("views/week.py", label="Back to my week", icon=":material/edit_calendar:")
right.page_link("views/results.py", label="Back to my results", icon=":material/bedtime:")
