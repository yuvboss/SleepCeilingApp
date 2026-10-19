from streamlit.testing.v1 import AppTest


def test_app_starts_on_the_introduction():
    at = AppTest.from_file("app.py").run()
    assert not at.exception
    assert at.title[0].value == "Introduction the Sleep Planner App"


def test_entry_screen_waits_for_the_time_helpers():
    at = AppTest.from_file("app.py").run()
    at.switch_page("views/week.py").run()
    assert not at.exception
    assert "time_helpers.py" in at.warning[0].value
