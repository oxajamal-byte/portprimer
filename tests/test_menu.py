from argparse import Namespace

from portprimer import menu
from portprimer.scanner import ScanResult


def test_authorized_website_requires_authorized_token(monkeypatch):
    answers = iter(["example.com", "yes"])
    monkeypatch.setattr(menu.console, "input", lambda _: next(answers))

    assert menu.authorized_website_scan() == 0


def test_authorized_website_routes_with_web_profile_and_public_allowed(monkeypatch):
    captured = {}
    answers = iter(["example.com", "AUTHORIZED"])
    monkeypatch.setattr(menu.console, "input", lambda _: next(answers))

    def fake_run(args: Namespace, profile_override: str | None = None) -> int:
        captured["args"] = args
        captured["profile_override"] = profile_override
        return 0

    monkeypatch.setattr(menu, "run_authorized_scan", fake_run)

    assert menu.authorized_website_scan() == 0
    assert captured["args"].target == "example.com"
    assert captured["args"].profile == "web"
    assert captured["args"].i_have_permission is True
    assert captured["args"].allow_public_target is True
    assert captured["args"].ask_explain is False
    assert captured["profile_override"] is None


def test_menu_routes_playground_choice(monkeypatch):
    answers = iter(["1", "q"])
    calls = []
    monkeypatch.setattr(menu.console, "input", lambda _: next(answers))
    monkeypatch.setattr(menu, "interactive_playground", lambda compact_logo=False: calls.append(compact_logo) or menu.InteractiveResult(lambda: None, []))

    assert menu.run_menu(no_clear=True) == 0
    assert calls == [False]


def test_menu_does_not_prompt_to_return_or_show_old_notes_prompt(monkeypatch):
    prompts = []
    answers = iter(["9", "q"])
    monkeypatch.setattr(menu.console, "input", lambda prompt: prompts.append(prompt) or next(answers))
    monkeypatch.setattr(menu, "interactive_demo", lambda compact_logo=False: menu.InteractiveResult(lambda: None, []))

    assert menu.run_menu(no_clear=True) == 0
    assert "Press Enter to return to the main menu..." not in prompts
    assert r"Show short learning notes now? \[y/N]: " not in prompts
    assert "Select: " in prompts


def test_menu_choice_m_returns_to_main_menu(monkeypatch):
    answers = iter(["1", "m", "0"])
    calls = []
    monkeypatch.setattr(menu.console, "input", lambda _: next(answers))
    monkeypatch.setattr(menu, "interactive_playground", lambda compact_logo=False: calls.append("playground") or menu.InteractiveResult(lambda: None, []))

    assert menu.run_menu(no_clear=True) == 0
    assert calls == ["playground"]


def test_learning_notes_not_forced_from_next_menu(monkeypatch):
    calls = []
    answers = iter(["q"])
    result = menu.InteractiveResult(lambda: result, [ScanResult(8022, "open")])
    monkeypatch.setattr(menu.console, "input", lambda _: next(answers))
    monkeypatch.setattr(menu, "learning_cards", lambda results: calls.append(results))

    assert menu._next_menu(result, no_clear=True, compact_logo=False) is False
    assert calls == []


def test_invalid_yes_no_reprompts_once_then_defaults_no(monkeypatch):
    answers = iter(["maybe", "still-nope"])
    monkeypatch.setattr(menu.console, "input", lambda _: next(answers))

    assert menu._confirm("Continue?") is False


def test_next_menu_choice_l_shows_learning_notes(monkeypatch):
    calls = []
    answers = iter(["l", "q"])
    result = menu.InteractiveResult(lambda: result, [ScanResult(8022, "open")])
    monkeypatch.setattr(menu.console, "input", lambda _: next(answers))
    monkeypatch.setattr(menu, "learning_cards", lambda results: calls.append(results))

    assert menu._next_menu(result, no_clear=True, compact_logo=False) is False
    assert calls == [[ScanResult(8022, "open")]]


def test_next_menu_n_returns_to_main_menu(monkeypatch):
    calls = []
    result = menu.InteractiveResult(lambda: result, [ScanResult(8022, "open")])
    monkeypatch.setattr(menu.console, "input", lambda _: "n")
    monkeypatch.setattr(menu, "learning_cards", lambda results: calls.append(results))

    assert menu._next_menu(result, no_clear=True, compact_logo=False) is True
    assert calls == []


def test_next_menu_choice_m_returns_to_main_menu(monkeypatch):
    result = menu.InteractiveResult(lambda: result, [ScanResult(8022, "open")])
    monkeypatch.setattr(menu.console, "input", lambda _: "m")

    assert menu._next_menu(result, no_clear=True, compact_logo=False) is True


def test_next_menu_enter_defaults_to_main_menu(monkeypatch):
    result = menu.InteractiveResult(lambda: result, [ScanResult(8022, "open")])
    monkeypatch.setattr(menu.console, "input", lambda _: "")

    assert menu._next_menu(result, no_clear=True, compact_logo=False) is True


def test_next_menu_no_open_services_hides_learning_notes(monkeypatch, capsys):
    result = menu.InteractiveResult(lambda: result, [ScanResult(80, "closed")])
    monkeypatch.setattr(menu.console, "input", lambda _: "q")

    assert menu._next_menu(result, no_clear=True, compact_logo=False) is False
