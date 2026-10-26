# Entry point: `streamlit run app.py` starts here.
#
# Streamlit re-runs this whole file from the top every time the user clicks or types anything.
# Normal variables are reset on every re-run; st.session_state is the one place that survives,
# so the user's week is kept there. This file:
#   1. creates the week in session state (once per browser tab),
#   2. draws the sidebar (save/load) that appears on every screen,
#   3. hands over to whichever screen the user is on (views/intro.py, week.py or results.py).
import streamlit as st

from storage import empty_week, week_from_json, week_to_json

st.set_page_config(page_title="Sleep Ceiling", page_icon="🌙")

# THE WEEK. Every screen reads and writes this same dictionary. Its exact shape is described at
# the top of storage.py. It starts empty; views/week.py fills it as the user enters activities.
# It belongs to one browser tab and is lost on refresh, which is why save/load exists.
if "week" not in st.session_state:
    st.session_state.week = empty_week()


# --- Sidebar: save and load the week as a JSON file ---

def load_uploaded_week():
    """Runs when the user picks a file to upload: replaces the week with the one in the file."""
    file = st.session_state.week_upload
    if file is None:
        return
    try:
        st.session_state.week = week_from_json(file.getvalue().decode("utf-8"))
    except ValueError as e:
        st.session_state.load_message = ("error", str(e))
        return
    # Make the wake-time widgets pick up the loaded values instead of keeping their old ones.
    for key in ["wake_input"] + [f"wake_{day}" for day in st.session_state.week["wake"]]:
        st.session_state.pop(key, None)
    st.session_state.load_message = ("success", f"Loaded {file.name}.")


# --- Navigation: the three screens from the project context, section 3, plus the two outcome
# screens the results screen sends people to (see flow.py) ---
# Every page is always registered (so the app can switch to it), but Streamlit's own page list is
# hidden. The sidebar below shows only the pages the user has reached: Results after "Get results",
# and the outcome screens once the results send them there. flow.py sets these flags.
intro_page = st.Page("views/intro.py", title="Introduction", icon=":material/home:", default=True)
week_page = st.Page("views/week.py", title="Enter your week", icon=":material/edit_calendar:")
results_page = st.Page("views/results.py", title="Results", icon=":material/bedtime:")
good_job_page = st.Page("views/good_job.py", title="Good job", icon=":material/check_circle:")
schedule_page = st.Page("views/updated_schedule.py", title="Updated schedule", icon=":material/event_available:")

navigation = st.navigation(
    [intro_page, week_page, results_page, good_job_page, schedule_page], position="hidden"
)

with st.sidebar:
    st.markdown("## 🌙 Sleep Ceiling")
    st.page_link(intro_page)
    st.page_link(week_page)
    if st.session_state.get("show_results"):
        st.page_link(results_page)
    if st.session_state.get("show_good_job"):
        st.page_link(good_job_page)
    if st.session_state.get("show_updated_schedule"):
        st.page_link(schedule_page)
    st.divider()

    st.markdown("**Save or load your week**")
    st.caption("Your week isn't stored online. Download it to keep it, and load it next time.")
    st.download_button(
        "Download week",
        week_to_json(st.session_state.week),
        file_name="my-week.json",
        mime="application/json",
        icon=":material/download:",
    )
    st.file_uploader("Load a saved week", type="json", key="week_upload", on_change=load_uploaded_week)
    message = st.session_state.pop("load_message", None)
    if message:
        kind, text = message
        if kind == "success":
            st.success(text)
        else:
            st.error(text)

navigation.run()
