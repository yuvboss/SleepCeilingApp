import streamlit as st

# Screen 1 — Introduction. The text is Saro's (from Introductionpage.txt, spelling and grammar
# fixed); the layout and styling are Claude's.

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;700&family=Rubik+Bubbles&display=swap');
    .intro-hero { text-align: center !important; padding: 1.5rem 0 1rem; }
    .intro-hero div { text-align: center !important; }
    div.intro-title {
        font-family: 'Rubik Bubbles', 'Fredoka', sans-serif !important;
        font-weight: 400 !important;   /* the font only comes in one weight; faking bold makes it jagged */
        font-synthesis: none;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        font-size: clamp(3rem, 9vw, 5.25rem) !important;
        line-height: 1.05 !important;
    }
    div.intro-tagline {
        font-family: 'Fredoka', sans-serif !important;
        font-weight: 700 !important;
        font-size: clamp(1.15rem, 3.2vw, 1.5rem) !important;
        margin-top: 0.6rem;
    }
    div.intro-goal { font-size: 1.05rem !important; opacity: 0.7; margin-top: 0.8rem; }
    .intro-step h4 { font-family: 'Fredoka', sans-serif; margin-top: 0; }
    </style>
    <div class="intro-hero">
        <div class="intro-title">Introducing Sleep Ceiling</div>
        <div class="intro-tagline">The app that helps you reach your sleeping potential!</div>
        <div class="intro-goal">Our goal is to help you maximize your sleep while maintaining a balanced schedule.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

st.subheader("Why does sleep matter for teenagers?")
st.write(
    "Sleep is important to all ages, but there is one group that needs it the most yet gets it the "
    "least. This age group, teenagers, needs around 8–10 hours of sleep a night, but about three in "
    "four US high schoolers sleep under 8 hours on an average school night. For them, this lack of "
    "sleep is associated with trouble concentrating, erratic changes in mood, a weakened immune "
    "system, and even physical issues like decreases in motor control, hand-eye coordination, "
    "balance, and overall physical endurance."
)
st.write(
    "On the surface, this lack of sleep seems like their fault, but in reality many of these kids "
    "have packed schedules with many activities that take up all their time and, in most cases, make "
    "them lose sleep. Schedules like this can be a huge problem if they're not tracked and "
    "maintained. That's where this app comes in."
)

st.subheader("How Sleep Ceiling helps")
st.write(
    "Sleep Ceiling solves this sleep and schedule problem by finding your predicted sleep time from "
    "your average weekly schedule and comparing it to your actual sleep time. It then gives you an "
    "updated schedule based on the results, which optimizes your schedule to hit your "
    "\"sleep ceiling\"."
)

st.subheader("How it works")
steps = [
    (
        "1. Entering your week",
        "This is the initial stage, where the app gets all the information about the user's "
        "activities, like the days they are on, starting time, ending time, importance, and "
        "malleability. This is also where the user sets their wake-up times.",
    ),
    (
        "2. Seeing the ceiling",
        "This is the second step to finding your optimal schedule for sleep. During this stage, the "
        "app will display your predicted sleep for each day and will allow the user to input their "
        "actual sleep for the corresponding days. This takes us to the final stage of the app.",
    ),
    (
        "3. Finding the cuts",
        "This is when you will finally be able to see your optimized schedule and the sleep you will "
        "be getting with it. Using this, we want to help you get a visual of the \"best\" sleep you "
        "can be getting so that you can actually achieve this goal.",
    ),
]
for column, (title, text) in zip(st.columns(3), steps):
    with column.container(border=True):
        st.markdown(f"<div class='intro-step'><h4>{title}</h4></div>", unsafe_allow_html=True)
        st.write(text)

st.divider()
st.markdown("<p style='text-align:center; font-size:1.1rem;'>Click here and get started now:</p>",
            unsafe_allow_html=True)
_, middle, _ = st.columns([1, 1, 1])
if middle.button("Enter your week", type="primary", use_container_width=True):
    st.switch_page("views/week.py")
