import streamlit as st

from storage import empty_week, week_from_json, week_to_json

st.set_page_config(page_title="Sleep Planner", page_icon="🌙")

# The whole week lives in the session: {"wake": minutes since midnight or None, "activities": [...]}
if "week" not in st.session_state:
    st.session_state.week = empty_week()


def load_uploaded_week():
    file = st.session_state.week_upload
    if file is None:
        return
    try:
        st.session_state.week = week_from_json(file.getvalue().decode("utf-8"))
    except ValueError as e:
        st.session_state.load_message = ("error", str(e))
        return
    # Make the wake-time widget pick up the loaded value instead of keeping its old one.
    st.session_state.pop("wake_input", None)
    st.session_state.load_message = ("success", f"Loaded {file.name}.")


with st.sidebar:
    st.subheader("Save or load your week")
    st.download_button(
        "Download week",
        week_to_json(st.session_state.week),
        file_name="my-week.json",
        mime="application/json",
    )
    st.file_uploader("Load a saved week", type="json", key="week_upload", on_change=load_uploaded_week)
    message = st.session_state.pop("load_message", None)
    if message:
        kind, text = message
        if kind == "success":
            st.success(text)
        else:
            st.error(text)

pages = [
    st.Page("views/intro.py", title="Introduction", default=True),
    st.Page("views/week.py", title="Enter your week"),
    st.Page("views/results.py", title="Results"),
]
st.navigation(pages).run()
