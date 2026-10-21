from streamlit.testing.v1 import AppTest


def test_app_starts_on_the_introduction():
    at = AppTest.from_file("app.py").run()
    assert not at.exception
    assert at.title[0].value == "Introduction the Sleep Planner App"


def test_entry_screen_shows_the_form():
    at = AppTest.from_file("app.py").run()
    at.switch_page("views/week.py").run()
    assert not at.exception
    assert not at.warning
    assert at.time_input(key="wake_input").label.startswith("Wake-up time")
