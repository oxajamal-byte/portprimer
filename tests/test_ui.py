from io import StringIO

from rich.console import Console

from portprimer import ui
from portprimer.scanner import ScanResult


def test_ascii_banner_strings_exist():
    assert "___           _   ___" in ui.ASCII_BANNER
    assert "ports explained, not exploited" in ui.ASCII_BANNER
    assert ui.COMPACT_BANNER == "PORTPRIMER\nports explained, not exploited"


def test_clear_screen_helper_does_not_crash():
    ui.clear_screen(no_clear=True)


def test_full_banner_used_at_sixty_columns(monkeypatch):
    output = StringIO()
    monkeypatch.setattr(ui, "console", Console(file=output, force_terminal=False, width=60))

    ui.title_header()

    rendered = output.getvalue()
    assert "___           _   ___" in rendered
    assert "PORTPRIMER" not in rendered


def test_compact_banner_not_automatic_below_sixty_columns(monkeypatch):
    output = StringIO()
    monkeypatch.setattr(ui, "console", Console(file=output, force_terminal=False, width=59))

    ui.title_header()

    rendered = output.getvalue()
    assert "___           _   ___" in rendered
    assert "PORTPRIMER" not in rendered


def test_compact_banner_only_when_requested(monkeypatch):
    output = StringIO()
    monkeypatch.setattr(ui, "console", Console(file=output, force_terminal=False, width=100))

    ui.title_header(compact_logo=True)

    rendered = output.getvalue()
    assert "PORTPRIMER" in rendered
    assert "___           _   ___" not in rendered


def test_no_open_services_output_has_no_fake_table_row(monkeypatch):
    output = StringIO()
    monkeypatch.setattr(ui, "console", Console(file=output, force_terminal=False, width=100))

    ui.results_table([ScanResult(80, "closed")])

    rendered = output.getvalue()
    assert "No open services found in this scan set." in rendered
    assert "| - " not in rendered
    assert "No open services were found in this scan set" not in rendered


def test_report_paths_print_on_separate_lines(monkeypatch):
    output = StringIO()
    monkeypatch.setattr(ui, "console", Console(file=output, force_terminal=False, width=80))

    ui.report_path_panel("reports/example.md", "reports/example.json")

    rendered = output.getvalue()
    assert "Reports saved" in rendered
    assert "Markdown: reports/example.md" in rendered
    assert "JSON:     reports/example.json" in rendered
