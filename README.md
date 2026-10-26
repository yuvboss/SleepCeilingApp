# Sleep Ceiling

**A sleep-first schedule app for teenagers.** Enter a typical week once, and the app works out how much sleep that week actually leaves room for, night by night. It then compares that with how much you really sleep and tells you what to do next.

Congressional App Challenge 2026 · California's 15th district · Saro, Carlmont High School

<!-- TODO before submitting: add the demo video link -->
- **Live app:** [sleepceilingapp-hoh7zobihqmz6pdmdlo5bm.streamlit.app](https://sleepceilingapp-hoh7zobihqmz6pdmdlo5bm.streamlit.app)
- **Demo video:** _link_

---

## The problem

Most teenagers who are short on sleep aren't making bad decisions at 11 PM. They've agreed to more than their week has room for, and nothing ever shows them that.

<!-- TODO: verify each figure against its source before submitting (see "Sources" below) -->
- The American Academy of Sleep Medicine recommends **8–10 hours a night** for ages 13–18.
- In the CDC's 2025 Youth Risk Behavior Survey, only about **24% of US high school students** got 8 or more hours on an average school night.
- That share falls through high school, from about 31% of ninth graders to 20% of seniors. That pattern points to a **scheduling problem, not a discipline problem**.

The app can't assume a teenager can simply go to bed earlier. At puberty the body clock shifts later, so there's a floor under how early a realistic bedtime is. That leaves one lever a student actually controls: **freeing up hours in the evening**. This app works that lever.

## What the app does

1. **Enter your week.** Add your recurring activities (school, practice, homework, a job, clubs, a commute) on the days they happen, with start and end times. Set your wake-up time, with a different time for any morning that differs, like weekends. Rate each activity's **importance** from 1 (expendable) to 5 (untouchable).
2. **See your predicted sleep.** For each night, the app measures from the end of that evening's last activity to the next morning's wake time. Almost nobody knows this number for their own week.
3. **Enter your actual sleep.** You type in what you really sleep each night, *after* you've seen the prediction.
4. **Get one clear answer.** Each night is green at **8 h 30 min** or more and red below it, for both predicted and actual sleep:
   - **All green:** your week works, and the app says so plainly.
   - **Predicted and actual don't match on a night:** the week as entered is probably incomplete (phone time, homework running over, anything that didn't feel worth logging). The app sends you back to add it and recompute. After two rounds it stops and asks one question: how long it takes you to fall asleep. Over 30 minutes, it suggests raising that with a doctor.
   - **A night is red for both:** the week genuinely doesn't have enough hours. The app goes to an **Updated schedule** that shortens or cuts activities to make room for sleep.

## How the Updated schedule works

The recommender uses the importance ratings you gave to decide what can change:

| Importance | What happens on a short night |
|---|---|
| 5 · Untouchable | Never changed |
| 4 · High | Shortened to 75% of its length |
| 3 · Medium | Shortened to 50% |
| 2 · Low | Shortened to 25% |
| 1 · Expendable | Removed |

For every night below 8 h 30 min, it looks at the activities on the evening that sets that night and shortens each one to its floor, once. Activities marked as movable within the day slide earlier to close the gap, so the time saved moves bedtime earlier and becomes sleep.

The Updated schedule screen shows each day's new activities and the sleep that night, next to how much it changed. You can then **adjust any start or end time yourself** and see your sleep recalculate straight away, or reset to the recommendation.

## Design decisions

| Decision | Why |
|---|---|
| A **typical week**, not a calendar | No dates or time zones to manage, and the advice applies from now on instead of to a week that's already half over. |
| A night is **named by the morning it ends** | Monday's sleep is decided by Sunday evening. Getting this wrong gives numbers that look plausible but are off by a day. The tests check it explicitly. |
| Target of **8 h 30 min** | The bottom of the American Academy of Pediatrics' 8.5–9.5 hour optimal range for teenagers: a sensible aim rather than the bare minimum. |
| **One importance rating** drives both shortening and cutting | Keeps the form short, and avoids two settings that could contradict each other. |
| **Wake time per morning** | Nobody wakes at 6:40 on a Saturday. Per-day wake times mean weekends need no special case. |
| A mismatch means **the week is incomplete**, not a lecture | Once phone time is entered as an activity rated 1, the recommender can cut it through the same mechanism as everything else. |
| **No accounts, no database** | Your week stays in your browser session. You can download it as a file and load it again later. Nothing about you is stored on a server. |
| **Always shorten to the floor**, then let you adjust | Gives the most sleep the week allows. You know your week best, so you can then give back time where it matters. |
| **No sleep-hygiene advice or gamification** | The app changes schedules. It gives one diagnosis and one set of changes: no badges, streaks or tips. |

## Built with

- **Python 3.9+** and **[Streamlit](https://streamlit.io)** 1.50
- Deployed on **Streamlit Community Cloud** from this repository
- **pytest** for automated tests

## Run it yourself

```bash
git clone https://github.com/yuvboss/SleepPlannerApp.git
cd SleepPlannerApp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501.

**Run the tests:**

```bash
pip install -r requirements-dev.txt
python -m pytest tests
```

## Project structure

| File | What it does |
|---|---|
| `app.py` | Starts the app: holds the week in the session, draws the sidebar, and switches between screens |
| `views/intro.py` | Screen 1: why sleep matters |
| `views/week.py` | Screen 2: enter your week (activity grid, pop-up form, wake times) |
| `views/results.py` | Screen 3: predicted vs. actual sleep, coloured, and the Proceed button |
| `views/good_job.py` | Shown when every night is green |
| `views/updated_schedule.py` | Shown when the week needs changes: the updated schedule, sleep per night, and times you can adjust |
| `time_helpers.py` | Converting clock times to minutes and back, and activity length across midnight |
| `sleep_calc.py` | **The available-sleep calculation:** seven nights, in minutes |
| `diagnosis.py` | **The decision:** all green, mismatch, or red on both, plus the limit of two send-backs |
| `recommender.py` | **The recommender:** shortens or cuts activities on short nights |
| `flow.py` | Moving between screens, and the fall-asleep question |
| `widgets.py` | The AM/PM time picker |
| `storage.py` | The shape of a saved week, and saving/loading it as a JSON file |
| `tests/` | Automated tests, including the off-by-one-day check and activities that cross midnight |

All times are stored as whole minutes since midnight. That keeps the arithmetic exact and makes activities that cross midnight easy to handle.

## Use of AI (disclosure)

The Congressional App Challenge allows AI assistance as long as it is disclosed and isn't the whole of the technical work. I used **Claude Code** (Anthropic) throughout this project, under a written split of who does what that I set at the start.

<!-- TODO: read this section carefully and correct anything that doesn't match what you did -->
**I wrote, myself:**
- the time helpers: converting clock times to minutes and back, and activity length with the midnight correction (`time_helpers.py`)
- the available-sleep calculation, including activities that cross midnight, per-day wake times, and naming each night by its morning (`sleep_calc.py`)
- the results logic: guards for missing data, the table, colouring each night against the 8 h 30 min target (`views/results.py`)
- the decision of where the user goes next, and the limit of two send-backs before the fall-asleep question (`diagnosis.py`)
- the recommender: finding short nights, shortening to each activity's floor, sliding movable activities and cutting importance-1 activities (`recommender.py`)
- the introduction text (Claude fixed spelling and grammar)
- every design decision listed above

**Claude wrote:**
- the project setup and the app's structure: navigation, the sidebar, and saving/loading the week as a file (`app.py`, `storage.py`, `flow.py`)
- the week-entry screen's form, grid and wake-time pickers (`views/week.py`, `widgets.py`)
- the input boxes and hours display on the results screen, and the Proceed button
- the Updated schedule screen's layout and the editing of times (`views/updated_schedule.py`)
- the Good job screen, including its text, at my request (`views/good_job.py`)
- the fall-asleep question's pop-up and its two messages (`flow.py`)
- the layout of the introduction page, and the visual design of the whole app
- the automated tests in `tests/`
- this README, with input and directions from me

**How I used it otherwise:** Claude explained Python and Streamlit concepts as I needed them (loops, functions, dictionaries, imports), ran my code against test cases, and pointed out bugs and edge cases for me to fix. It was told not to write the core logic, and it didn't.

## Limitations

- Sleep research shows **associations, not causation**. Short sleep goes along with workload, stress and screen use.
- Actual sleep is **self-reported**.
- The app models a **typical week**. Unusual weeks need to be entered separately.
- Moving an activity to a **different day** is out of scope for this version.
- An activity is shortened or cut on **every day it's on**, including days whose nights were already long enough.
- The recommender shortens to each activity's floor rather than only as much as needed. You can adjust the times afterwards.

## Sources

<!-- TODO: open each source and confirm the figures before submitting -->
- Paruthi et al., *Recommended Amount of Sleep for Pediatric Populations*, Journal of Clinical Sleep Medicine, 2016 (American Academy of Sleep Medicine consensus statement)
- American Academy of Pediatrics, *School Start Times for Adolescents*, Pediatrics 134(3), 2014
- Centers for Disease Control and Prevention, Youth Risk Behavior Survey, 2025
- Crowley, Acebo and Carskadon, *Sleep, circadian rhythms, and delayed phase in adolescence*, Sleep Medicine, 2007
- Dunster et al., *Sleepmore in Seattle: Later school start times are associated with more sleep and better performance in high school students*, Science Advances, 2018
