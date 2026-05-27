from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.progress import Progress, TextColumn, TimeElapsedColumn
from rich.text import Text

from .knowledge import get_port_knowledge
from .report import summarize_results
from .scanner import ScanResult

console = Console()
RULE = "-" * 40
ASCII_BANNER = r""" ___           _   ___      _
| _ \___ _ _| |_| _ \_ _(_)_ __  ___ _ _
|  _/ _ \ '_|  _|  _/ '_| | '  \/ -_) '_|
|_| \___/_|  \__|_| |_| |_|_|_|_\___|_|

        ports explained, not exploited"""
COMPACT_BANNER = "PORTPRIMER\nports explained, not exploited"

SERVICE_DISPLAY_NAMES = {
    8080: "HTTP Alt",
    1433: "MSSQL",
    5432: "Postgres",
    8022: "Playground SSH",
    15432: "Playground DB",
    16379: "Playground Cache",
    18080: "Playground Web",
}


def clear_screen(no_clear: bool = False) -> None:
    if no_clear:
        return
    console.clear()

ACTION_DISPLAY_NAMES = {
    "Usually okay if expected": "Expected",
    "Review if unexpected": "Review",
    "Keep private": "Private",
    "Replace or disable if unused": "Disable if unused",
    "Lab only": "Lab only",
    "Learn more before changing": "Learn first",
}

NOTE_LINES = {
    8022: (
        "Safe local practice service.",
        "Shows how an admin-style open port appears.",
        "Localhost only. Not a real SSH service.",
    ),
    8080: (
        "Alternate web port; local practice in Playground Tour.",
        "Shows how a web-style open port appears.",
        "Inspect real services only with permission.",
    ),
    15432: (
        "Safe local practice service.",
        "Shows how a data-style open port appears.",
        "Localhost only. Not a real database.",
    ),
    16379: (
        "Safe local practice service.",
        "Shows how a cache-style open port appears.",
        "Localhost only. Not Redis.",
    ),
    18080: (
        "Safe local practice service.",
        "Shows how a web-style open port appears.",
        "Localhost only. Not a real web service.",
    ),
}


def title_header(compact_logo: bool = False) -> None:
    console.print()
    if compact_logo:
        name, tagline = COMPACT_BANNER.splitlines()
        console.print(Text(name, style="bold #d7b56d"))
        console.print(Text(tagline, style="dim"))
    else:
        lines = ASCII_BANNER.splitlines()
        console.print(Text("\n".join(lines[:5]), style="bold #d7b56d"))
        console.print()
        console.print(Text(lines[-1], style="dim"))
    console.print(f"[dim]{RULE}[/]")


def title_panel() -> None:
    title_header()


def session_context(mode: str, target: str, profile: str, ports: list[int], timeout: float, concurrency: int, note: str | None = None) -> None:
    console.print()
    console.print(f"[#d7b56d]Scan:[/] {mode}")
    console.print(f"[#d7b56d]Target:[/] {target}")
    console.print(f"[#d7b56d]Profile:[/] {profile}")
    console.print(f"[#d7b56d]Checked:[/] {len(ports)} ports")
    if note:
        console.print(f"[dim]{note}[/]")


def learning_path_panel(text: str) -> None:
    console.print()
    console.print(text)


def settings_panel(target: str, profile: str, ports: list[int], timeout: float, concurrency: int) -> None:
    session_context("Scan", target, profile, ports, timeout, concurrency)


def responsible_use_panel() -> None:
    console.print("[#d7b56d]Scope:[/] [dim]Scan only systems you own or have permission to test.[/]\n")


def progress() -> Progress:
    return Progress(TextColumn("[#d7b56d]{task.description}"), TimeElapsedColumn(), console=console)


def _display_service(port: int, service: str) -> str:
    return SERVICE_DISPLAY_NAMES.get(port, service[:20])


def _display_action(action_hint: str) -> str:
    return ACTION_DISPLAY_NAMES.get(action_hint, action_hint[:16])


def _short_note(text: str, limit: int = 60) -> str:
    first_sentence = text.split(". ", 1)[0].strip()
    if first_sentence and not first_sentence.endswith("."):
        first_sentence += "."
    candidate = first_sentence or text.strip()
    if len(candidate) <= limit:
        return candidate
    trimmed = candidate[: limit - 3].rsplit(" ", 1)[0].rstrip(".,;:")
    return f"{trimmed}..."


def results_table(results: list[ScanResult]) -> None:
    open_results = [result for result in results if result.status == "open"]
    summary = summarize_results(results)
    console.print(f"[#d7b56d]Open:[/] [green]{summary['open']}[/]")
    console.print()

    if not open_results:
        console.print("[#f3ead7]No open services found in this scan set.[/]\n")
        return

    console.print("[#f3ead7]Open services[/]")
    console.print(f"[dim]{RULE}[/]")
    for result in open_results:
        knowledge = get_port_knowledge(result.port)
        service = _display_service(result.port, knowledge.service)
        action = _display_action(knowledge.action_hint)
        console.print(
            f"[#f3ead7]{result.port:<6}[/] "
            f"[#f3ead7]{service:<20}[/] "
            f"[#b58bdc]{knowledge.learning_label:<11}[/] "
            f"[#d7b56d]{action}[/]"
        )
    console.print()


def learning_cards(results: list[ScanResult]) -> None:
    for result in results:
        if result.status != "open":
            continue
        knowledge = get_port_knowledge(result.port)
        what, why, note = NOTE_LINES.get(
            result.port,
            (
                _short_note(knowledge.purpose),
                _short_note(knowledge.used_for),
                _short_note(knowledge.beginner_takeaway),
            ),
        )
        console.print(f"[#f3ead7]{result.port}/tcp {_display_service(result.port, knowledge.service)}[/]")
        console.print(f"  [#d7b56d]What:[/] {what}")
        console.print(f"  [#d7b56d]Use:[/]  {why}")
        console.print(f"  [#d7b56d]Watch:[/] {_short_note(knowledge.common_misuse_or_attack)}")
        console.print(f"  [#d7b56d]Takeaway:[/] {note}")
        console.print()


def report_path_panel(markdown_path: Path, json_path: Path) -> None:
    markdown_text = str(markdown_path).replace("\\", "/")
    json_text = str(json_path).replace("\\", "/")
    console.print("[green]Done.[/]")
    console.print("[green]Reports saved[/]")
    console.print(f"  [#d7b56d]Markdown:[/] {markdown_text}")
    console.print(f"  [#d7b56d]JSON:    [/] {json_text}")
