"""Moving the user between screens, with a message to show when they arrive.

Plumbing only: WHEN to send someone somewhere, and what the message says, is decided by the
results screen (student's logic). These functions just do the move.
"""
import streamlit as st


def send_back_to_week(message):
    """Go to the "Enter your week" screen and show `message` there in a pop-up."""
    st.session_state.week_message = message
    st.switch_page("views/week.py")


def go_to_results():
    """Go to the "Results" screen, and show it in the sidebar from now on."""
    st.session_state.show_results = True
    st.switch_page("views/results.py")


def go_to_good_job():
    """Go to the "Good job" screen, and show it in the sidebar from now on."""
    st.session_state.show_good_job = True
    st.switch_page("views/good_job.py")


def go_to_updated_schedule():
    """Go to the "Updated schedule" screen, and show it in the sidebar from now on."""
    st.session_state.show_updated_schedule = True
    st.switch_page("views/updated_schedule.py")
