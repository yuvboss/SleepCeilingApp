import streamlit as st

st.title("SleepPlanner")

wake = st.time_input("What time do you wake up?")
target = st.slider("Sleep target (hours)", 6.0, 10.0, 8.0, 0.25)

if st.button("Show me"):
    st.write(f"Wake at {wake}, aiming for {target} hours.")