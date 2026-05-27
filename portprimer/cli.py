from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from .playground import playground_ports, playground_services
from .profiles import FULL_RANGE_PORTS, choose_ports, list_profiles
from .report import generate_demo_report, generate_metasploitable_demo_report, metasploitable_demo_results, write_reports
from .safety import PUBLIC_TARGET_AUTHORIZATION_MESSAGE, evaluate_full_range_permission, evaluate_scan_permission
from .scanner import scan_ports
from .scanner import ScanResult
from .ui import console, learning_cards, learning_path_panel, progress, report_path_panel, responsible_use_panel, results_table, session_context, title_header, title_panel
from .learning import run_learning_center
from .quiz import run_quiz


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="portprimer",
        description="Learn what open TCP ports mean with small, authorized scan paths.",
        epilog="Run without a command for the beginner-friendly interactive menu.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--no-clear", action="store_true", help="Disable screen clearing in interactive mode.")
    parser.add_argument("--compact-logo", action="store_true", help="Use the compact PORTPRIMER logo.")
    subparsers = parser.add_subparsers(dest="command")

    scan = subparsers.add_parser(
        "scan",
        help="Run an authorized TCP connect scan.",
        description="Scan one authorized target with a small profile or custom port list.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    scan.add_argument("--target", required=True, help="Target IP address or hostname you own or have permission to scan.")
    scan.add_argument("--profile", choices=list_profiles(), help="Port profile to scan. Defaults to beginner.")
    scan.add_argument("--ports", help="Comma-separated custom ports, maximum 100.")
    scan.add_argument("--timeout", type=float, default=1.0, help="TCP connect timeout in seconds.")
    scan.add_argument("--concurrency", type=int, default=50, help="Concurrent connection attempts, maximum 50.")
    scan.add_argument("--i-have-permission", action="store_true", help="Confirm that you are authorized to scan this target.")
    scan.add_argument("--allow-public-target", action="store_true", help="Allow a public target only when you own it or have written permission.")
    scan.add_argument("--explain", action="store_true", help="Show short learning notes after the open-services list.")
    scan.add_argument("--full-range", action="store_true", help="Scan TCP ports 1-65535 on localhost/private targets only.")

    lab = subparsers.add_parser(
        "lab",
        help="Run the Metasploitable 2 local lab profile.",
        description="Scan your own isolated Metasploitable 2 lab VM with the training profile.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    lab.add_argument("--target", required=True, help="Local isolated Metasploitable 2 VM IP.")
    lab.add_argument("--timeout", type=float, default=1.0, help="TCP connect timeout in seconds.")
    lab.add_argument("--concurrency", type=int, default=50, help="Concurrent connection attempts, maximum 50.")
    lab.add_argument("--i-have-permission", action="store_true", help="Confirm that this is your isolated lab VM.")
    lab.add_argument("--explain", action="store_true", help="Show short learning notes after the open-services list.")

    playground = subparsers.add_parser(
        "playground",
        help="Start the Playground Tour and scan safe local practice services.",
        description="Start harmless TCP listeners on 127.0.0.1 high ports, scan them, write reports, then shut them down.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    playground.add_argument("--timeout", type=float, default=1.0, help="TCP connect timeout in seconds.")
    playground.add_argument("--concurrency", type=int, default=10, help="Concurrent connection attempts, maximum 50.")
    playground.add_argument("--explain", action="store_true", help="Show short learning notes after the open-services list.")

    subparsers.add_parser("metasploitable-demo", help="Run a simulated Metasploitable-style learning tour without scanning.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers.add_parser("quiz", help="Run the 20-question port knowledge quiz.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers.add_parser("learn", help="Open the Port Learning Center.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers.add_parser("demo", help="Generate a sample report without scanning.", description="Write a sample Markdown and JSON report.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    return parser


def _confirm_explain() -> bool:
    for attempt in range(2):
        answer = console.input(r"Show short learning notes now? \[y/N]: ").strip().lower()
        if answer in {"", "n", "no"}:
            return False
        if answer in {"y", "yes"}:
            return True
        if attempt == 0:
            console.print("[#d7b56d]Please type y or n.[/]")
    return False


async def _run_scan(
    target: str,
    profile: str,
    ports: list[int],
    timeout: float,
    concurrency: int,
    show_title: bool = True,
    mode: str = "Authorized Scan",
    note: str | None = None,
    explain: bool = False,
    ask_explain: bool = False,
    compact_logo: bool = False,
) -> tuple[Path, Path, list[ScanResult]]:
    if show_title:
        title_header(compact_logo=compact_logo)
    session_context(mode, target, profile, ports, timeout, concurrency, note=note)
    responsible_use_panel()
    with progress() as scan_progress:
        task = scan_progress.add_task("Running TCP connect scan...", total=None)
        results = await scan_ports(target, ports, timeout=timeout, concurrency=concurrency)
        scan_progress.update(task, completed=1)
    results_table(results)
    if explain or (ask_explain and _confirm_explain()):
        learning_cards(results)
    markdown_path, json_path = write_reports(target, profile, results, timeout, concurrency)
    report_path_panel(markdown_path, json_path)
    return markdown_path, json_path, results


async def _run_playground(timeout: float, concurrency: int, explain: bool = False, ask_explain: bool = False, compact_logo: bool = False) -> tuple[Path, Path, list[ScanResult]]:
    _, ports = choose_ports("playground", None)
    if ports != playground_ports():
        raise ValueError("Playground profile does not match the local teaching service ports.")
    async with playground_services():
        title_header(compact_logo=compact_logo)
        return await _run_scan(
            "127.0.0.1",
            "playground",
            ports,
            timeout,
            concurrency,
            show_title=False,
            mode="Playground Tour",
            note="Safe local practice services are running on 127.0.0.1 only.",
            explain=explain,
            ask_explain=ask_explain,
            compact_logo=compact_logo,
        )


def run_authorized_scan(args: argparse.Namespace, profile_override: str | None = None) -> int:
    target = args.target
    if getattr(args, "full_range", False):
        if getattr(args, "ports", None) or getattr(args, "profile", None):
            console.print("[bold red]Error:[/] Use --full-range without --profile or --ports.")
            return 2
        profile, ports = "full-range", FULL_RANGE_PORTS
        decision = evaluate_full_range_permission(target, args.i_have_permission)
    else:
        profile, ports = choose_ports(profile_override or getattr(args, "profile", None), getattr(args, "ports", None))
        decision = evaluate_scan_permission(target, args.i_have_permission, getattr(args, "allow_public_target", False))
    if not decision.allowed:
        title_panel()
        if decision.reason == PUBLIC_TARGET_AUTHORIZATION_MESSAGE:
            console.print(decision.reason, soft_wrap=True)
        else:
            console.print(f"[bold red]Scan refused:[/] {decision.reason}")
        return 2
    try:
        asyncio.run(_run_scan(target, profile, ports, args.timeout, args.concurrency, explain=getattr(args, "explain", False), ask_explain=getattr(args, "ask_explain", False), compact_logo=getattr(args, "compact_logo", False)))
    except ValueError as exc:
        console.print(f"[bold red]Error:[/] {exc}")
        return 2
    return 0


def run_demo(compact_logo: bool = False) -> int:
    title_header(compact_logo=compact_logo)
    learning_path_panel("[bold]Demo Report[/]\n[dim]Generate a sample report without scanning.[/]")
    markdown_path, json_path = generate_demo_report()
    report_path_panel(markdown_path, json_path)
    return 0


def run_metasploitable_demo(compact_logo: bool = False, explain: bool = False) -> int:
    title_header(compact_logo=compact_logo)
    learning_path_panel("[bold]Metasploitable Demo Tour[/]\n[dim]Simulated learning session. No network scan is performed.[/]")
    results = metasploitable_demo_results()
    results_table(results)
    if explain:
        learning_cards(results)
    markdown_path, json_path = generate_metasploitable_demo_report()
    report_path_panel(markdown_path, json_path)
    return 0


def run_playground(args: argparse.Namespace) -> int:
    try:
        asyncio.run(_run_playground(args.timeout, args.concurrency, explain=getattr(args, "explain", False), ask_explain=getattr(args, "ask_explain", False), compact_logo=getattr(args, "compact_logo", False)))
    except OSError as exc:
        console.print(f"[bold red]Playground could not start:[/] {exc}")
        console.print("[yellow]One of the playground ports may already be in use on 127.0.0.1.[/]")
        return 2
    except ValueError as exc:
        console.print(f"[bold red]Error:[/] {exc}")
        return 2
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        from .menu import run_menu

        return run_menu(no_clear=args.no_clear, compact_logo=args.compact_logo)
    if args.command == "scan":
        try:
            return run_authorized_scan(args)
        except ValueError as exc:
            console.print(f"[bold red]Error:[/] {exc}")
            return 2
    if args.command == "lab":
        console.print("[#d7b56d]Metasploitable 2 lab mode is for an isolated local lab VM only.[/]")
        return run_authorized_scan(args, profile_override="metasploitable2")
    if args.command == "playground":
        return run_playground(args)
    if args.command == "metasploitable-demo":
        return run_metasploitable_demo(compact_logo=args.compact_logo)
    if args.command == "quiz":
        return run_quiz(compact_logo=args.compact_logo)
    if args.command == "learn":
        return run_learning_center(compact_logo=args.compact_logo)
    if args.command == "demo":
        return run_demo(compact_logo=args.compact_logo)
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
