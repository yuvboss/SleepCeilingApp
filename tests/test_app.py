from streamlit.testing.v1 import AppTest


def test_app_starts_on_the_introduction():
    at = AppTest.from_file("app.py").run()
    assert not at.exception
    assert any("Introducing Sleep Ceiling" in m.value for m in at.markdown)
    assert any(b.label == "Enter your week" for b in at.button)


def test_entry_screen_shows_the_form():
    at = AppTest.from_file("app.py").run()
    at.switch_page("views/week.py").run()
    assert not at.exception
    assert not at.warning
    assert at.selectbox(key="wake_input").label == "Usual wake-up time"
    assert at.selectbox(key="wake_Sat").label == "Sat"


def test_message_sent_back_to_the_entry_screen_shows_once():
    at = AppTest.from_file("app.py").run()
    at.session_state.week_message = "Your actual and predicted sleep don't match."
    at.switch_page("views/week.py").run()
    assert not at.exception
    assert any("don't match" in m.value for m in at.markdown)
    assert "week_message" not in at.session_state
    at.run()
    assert not any("don't match" in m.value for m in at.markdown)


def test_outcome_screens_open():
    for page in ["views/good_job.py", "views/updated_schedule.py"]:
        at = AppTest.from_file("app.py").run()
        at.switch_page(page).run()
        assert not at.exception


def sidebar_links(at):
    return [link.proto.label for link in at.sidebar.get("page_link")]


def test_sidebar_starts_with_only_intro_and_week():
    at = AppTest.from_file("app.py").run()
    assert sidebar_links(at) == ["Introduction", "Enter your week"]


def test_get_results_opens_results_and_adds_it_to_the_sidebar():
    at = AppTest.from_file("app.py").run()
    at.switch_page("views/week.py").run()
    [b for b in at.button if b.label == "Get results"][0].click().run()
    assert not at.exception
    assert at.title[0].value == "Results"
    assert sidebar_links(at) == ["Introduction", "Enter your week", "Results"]
