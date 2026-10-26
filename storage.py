"""The shape of a week, and saving/loading it as a JSON file the user downloads.

Nothing is written on the server (its filesystem is ephemeral); the file lives with the user.

THE WEEK (this is what st.session_state.week holds, and what your calculation reads):

    {
        "wake": {                # wake time for EACH MORNING, minutes since midnight. None until set.
            "Mon": 400,          #   Monday morning 6:40
            "Tue": 400,
            ...
            "Sat": 660,          #   Saturday morning 11:00 (overridden)
            "Sun": 660,
        },
        "wake_default": 400,     # the "usual" wake time the form fills every morning with. Only the
                                 #   form uses this; the calculation reads week["wake"][day].
        "activities": [          # every activity, each stored ONCE with the list of days it's on
            {
                "name": "Homework",       # as the user typed it
                "days": ["Mon", "Tue"],   # some of DAYS below, always in Mon..Sun order
                "start": 1260,            # minutes since midnight, 0..1439 (21:00)
                "end": 1380,              # minutes since midnight (23:00). Can be LESS than start:
                                          #   that means the activity runs past midnight.
                "importance": 3,          # 1..5. 5 = untouchable, 1 = can be cut. Used by the recommender.
                "malleable": False,       # could move to a different time in the SAME day
            },
        ],
    }
"""
import json

# The seven day codes used everywhere in the app. A day's position in this list is its day
# number: DAYS.index("Mon") == 0 ... DAYS.index("Sun") == 6.
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def empty_week():
    """A brand-new week with nothing entered. app.py puts this into st.session_state.week."""
    return {"wake": {day: None for day in DAYS}, "wake_default": None, "activities": []}


def week_to_json(week):
    """Turn the week into the text of the downloaded file (used by the sidebar's Download button)."""
    return json.dumps(week, indent=2)


def week_from_json(text):
    """Parse an uploaded week. Raises ValueError with a readable message if it doesn't match the data model."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"That isn't a valid JSON file ({e.msg}).")
    if not isinstance(data, dict) or not isinstance(data.get("activities"), list):
        raise ValueError("That file isn't a saved week.")

    wake = data.get("wake")
    default = data.get("wake_default")
    if wake is None or _is_minute(wake):
        # A file saved before wake times were per day: one time for every morning.
        default = wake
        wake = {day: wake for day in DAYS}
    if not isinstance(wake, dict) or set(wake) != set(DAYS):
        raise ValueError("The wake times must give one time for each day, Mon to Sun.")
    for day in DAYS:
        if wake[day] is not None and not _is_minute(wake[day]):
            raise ValueError(f"{day}: the wake time must be whole minutes since midnight, 0 to 1439.")
    if default is not None and not _is_minute(default):
        raise ValueError("The usual wake time must be whole minutes since midnight, 0 to 1439.")

    activities = [_check_activity(a, n) for n, a in enumerate(data["activities"], start=1)]
    return {"wake": {day: wake[day] for day in DAYS}, "wake_default": default, "activities": activities}


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _is_minute(v):
    return _is_int(v) and 0 <= v <= 1439


def _check_activity(a, n):
    if not isinstance(a, dict):
        raise ValueError(f"Activity {n} isn't in the right format.")
    name = a.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError(f"Activity {n} has no name.")
    days = a.get("days")
    if not isinstance(days, list) or not days or any(d not in DAYS for d in days):
        raise ValueError(f"{name}: days must be at least one of Mon, Tue, Wed, Thu, Fri, Sat, Sun.")
    for key in ("start", "end"):
        if not _is_minute(a.get(key)):
            raise ValueError(f"{name}: {key} must be whole minutes since midnight, 0 to 1439.")
    importance = a.get("importance")
    if not _is_int(importance) or not 1 <= importance <= 5:
        raise ValueError(f"{name}: importance must be a whole number from 1 to 5.")
    if not isinstance(a.get("malleable"), bool):
        raise ValueError(f"{name}: malleable must be true or false.")
    return {
        "name": name,
        "days": [d for d in DAYS if d in days],
        "start": a["start"],
        "end": a["end"],
        "importance": importance,
        "malleable": a["malleable"],
    }
