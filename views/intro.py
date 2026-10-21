import streamlit as st

# Screen 1 — Introduction. The copy on this page is yours to write (project context, section 3):
# why sleep matters for teenagers, a few statistics from section 9, then the button below.
st.title("Introduction the Sleep Planner App")

if st.button("Enter your week", type="primary"):
    st.switch_page("views/week.py")
