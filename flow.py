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


@st.dialog("One more question")
def ask_fall_asleep_question():
    """The question asked when the under-reporting loop stops (project context, section 5 + amendment A3).

    Over 30 minutes to fall asleep: suggest raising it with a doctor, and stop. Otherwise: the week
    probably still has unlogged time. No sleep advice either way (section 6).
    """
    st.write("When you get into bed, how long does it take you to fall asleep?")
    minutes = st.number_input(
        "Minutes to fall asleep", min_value=0, max_value=600, step=5, value=None, placeholder="minutes"
    )
    if st.button("Submit", type="primary"):
        if minutes is None:
            st.error("Enter a number of minutes.")
        elif minutes > 30:
            st.warning(
                "Regularly taking more than 30 minutes to fall asleep is worth raising with a doctor. "
                "That isn't something a schedule change can fix, so Sleep Ceiling stops here."
            )
        else:
            st.info(
                "Your week has room for the sleep you need, so some time is probably still missing from it. "
                "Add everything you do, including things that don't feel important, like time on your phone."
            )
            st.page_link("views/week.py", label="Go to Enter your week", icon=":material/edit_calendar:")
