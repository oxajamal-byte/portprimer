from argparse import Namespace
from io import StringIO
from pathlib import Path

from rich.console import Console

from portprimer import cli, ui
from portprimer.scanner import ScanResult


def _args(explain: bool) -> Namespace:
    return Namespace(
        target="127.0.0.1",
        profile="playground",
        ports=None,
        timeout=1.0,
        concurrency=10,
        i_have_permission=True,
        allow_public_target=False,
        explain=explain,
        ask_explain=False,
    )


def _scan_args(
    target: str,
    profile: str | None = "web",
    allow_public_target: bool = False,
    full_range: bool = False,
) -> Namespace:
    return Namespace(
        target=target,
        profile=profile,
        ports=None,
        timeout=1.0,
        concurrency=10,
        i_have_permission=True,
        allow_public_target=allow_public_target,
        explain=False,
        ask_explain=False,
        compact_logo=False,
        full_range=full_range,
    )


def test_public_scan_without_allow_public_target_refuses(monkeypatch):
    output = StringIO()
    test_console = Console(file=output, force_terminal=False, width=100)
    monkeypatch.setattr(ui, "console", test_console)
    monkeypatch.setattr(cli, "console", test_console)

    assert cli.run_authorized_scan(_scan_args("8.8.8.8", allow_public_target=False)) == 2
    rendered = output.getvalue()
    assert "Public target detected." in rendered
    assert "PortPrimer supports website/public-IP scans only when you own the target or have written permission." in rendered
    assert "Run again with --allow-public-target if this scan is authorized." in rendered
    assert "permanently blocked" not in rendered


def test_public_scan_with_allow_public_target_runs_web_profile(monkeypatch):
    captured = {}
    output = StringIO()
    test_console = Console(file=output, force_terminal=False, width=100)
    monkeypatch.setattr(ui, "console", test_console)
    monkeypatch.setattr(cli, "console", test_console)

    async def fake_scan_ports(target, ports, **kwargs):
        captured["target"] = target
        captured["ports"] = ports
        return [ScanResult(80, "closed")]

    def fake_write_reports(target, profile, results, timeout, concurrency):
        captured["profile"] = profile
        return Path("reports/a.md"), Path("reports/a.json")

    monkeypatch.setattr(cli, "scan_ports", fake_scan_ports)
    monkeypatch.setattr(cli, "write_reports", fake_write_reports)

    assert cli.run_authorized_scan(_scan_args("8.8.8.8", allow_public_target=True)) == 0
    assert captured["target"] == "8.8.8.8"
    assert captured["profile"] == "web"
    assert captured["ports"] == [80, 443, 8000, 8080, 8443]


def test_public_full_range_refuses_even_with_allow_public_target(monkeypatch):
    output = StringIO()
    test_console = Console(file=output, force_terminal=False, width=100)
    monkeypatch.setattr(ui, "console", test_console)
    monkeypatch.setattr(cli, "console", test_console)

    assert cli.run_authorized_scan(_scan_args("8.8.8.8", profile=None, allow_public_target=True, full_range=True)) == 2
    rendered = output.getvalue()
    assert "Full-range scans are local/private targets only" in rendered


def test_default_output_does_not_show_learning_notes(monkeypatch):
    output = StringIO()
    test_console = Console(file=output, force_terminal=False, width=80)
    monkeypatch.setattr(ui, "console", test_console)
    monkeypatch.setattr(cli, "console", test_console)

    async def fake_scan_ports(*args, **kwargs):
        return [ScanResult(8022, "open")]

    monkeypatch.setattr(cli, "scan_ports", fake_scan_ports)
    monkeypatch.setattr(cli, "write_reports", lambda *args, **kwargs: (Path("reports/a.md"), Path("reports/a.json")))

    assert cli.run_authorized_scan(_args(explain=False)) == 0
    rendered = output.getvalue()
    assert "Playground SSH" in rendered
    assert "What:" not in rendered


def test_explain_flag_shows_short_learning_notes(monkeypatch):
    output = StringIO()
    test_console = Console(file=output, force_terminal=False, width=80)
    monkeypatch.setattr(ui, "console", test_console)
    monkeypatch.setattr(cli, "console", test_console)

    async def fake_scan_ports(*args, **kwargs):
        return [ScanResult(8022, "open")]

    monkeypatch.setattr(cli, "scan_ports", fake_scan_ports)
    monkeypatch.setattr(cli, "write_reports", lambda *args, **kwargs: (Path("reports/a.md"), Path("reports/a.json")))

    assert cli.run_authorized_scan(_args(explain=True)) == 0
    rendered = output.getvalue()
    assert "8022/tcp Playground SSH" in rendered
    assert "What: Safe local practice service." in rendered
    assert "Use:  Shows how an admin-style open port appears." in rendered


def test_invalid_explain_prompt_defaults_no(monkeypatch):
    prompts = []
    answers = iter(["bad", "still-bad"])
    monkeypatch.setattr(cli.console, "input", lambda prompt: prompts.append(prompt) or next(answers))

    assert cli._confirm_explain() is False
    assert prompts == [r"Show short learning notes now? \[y/N]: ", r"Show short learning notes now? \[y/N]: "]


def test_no_clear_flag_is_accepted():
    parser = cli.build_parser()
    args = parser.parse_args(["--no-clear"])

    assert args.no_clear is True
    assert args.command is None


def test_compact_logo_flag_is_accepted():
    parser = cli.build_parser()
    args = parser.parse_args(["--compact-logo"])

    assert args.compact_logo is True
    assert args.command is None
