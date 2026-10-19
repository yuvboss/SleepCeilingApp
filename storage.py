"""Save and load the week as a JSON file the user downloads.

Nothing is written on the server (its filesystem is ephemeral); the file lives with the user.
"""
import json

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def empty_week():
    return {"wake": None, "activities": []}


def week_to_json(week):
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
    if wake is not None and not _is_minute(wake):
        raise ValueError("The wake time must be whole minutes since midnight, 0 to 1439.")

    activities = [_check_activity(a, n) for n, a in enumerate(data["activities"], start=1)]
    return {"wake": wake, "activities": activities}


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
