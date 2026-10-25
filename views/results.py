import streamlit as st

# Screen 3 — Results. This screen is yours (project context, sections 3 and 7): the Day / Actual /
# Predicted table, the colouring, the comparison and the diagnosis.
#
# WHERE THE DATA COMES FROM
#   week = st.session_state.week     # filled in on the "Enter your week" screen
#   week["wake"]["Mon"]              # Monday MORNING's wake time, int minutes, or None if not set
#   week["activities"]               # list of activity dicts (shape: top of storage.py)
#
# WHERE YOUR FUNCTIONS GO
#   Put the calculation in its own file (e.g. sleep_calc.py next to app.py), as a function that
#   takes the week dictionary and returns the seven nights, Mon..Sun, in minutes. Keep Streamlit
#   out of that file so it can be tested with a hand-written week. Then, here:
#       from sleep_calc import <your function>
#   call it with st.session_state.week and display the result.
#   The recommender and the diagnosis follow the same pattern: logic in its own file, shown here.

st.title("Results")
st.info("This screen hasn't been built yet.")
