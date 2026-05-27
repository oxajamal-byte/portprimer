from __future__ import annotations

import asyncio
from argparse import Namespace
from dataclasses import dataclass
from typing import Callable

from .cli import _run_playground, _run_scan, run_authorized_scan, run_demo, run_metasploitable_demo, run_playground
from .learning import run_learning_center
from .profiles import FULL_RANGE_PORTS, choose_ports, list_profiles
from .quiz import run_quiz
from .scanner import ScanResult
from .safety import evaluate_full_range_permission, evaluate_scan_permission
from .ui import clear_screen, console, learning_cards, title_header


@dataclass
class InteractiveResult:
    rerun: Callable[[], "InteractiveResult"]
    results: list[ScanResult]
    rerun_label: str = "run again"


def _confirm(prompt: str) -> bool:
    for attempt in range(2):
        answer = console.input(f"{prompt} [y/N]: ").strip().lower()
        if answer in {"", "n", "no"}:
            return False
        if answer in {"y", "yes"}:
            return True
        if attempt == 0:
            console.print("[#d7b56d]Please type y or n.[/]")
    return False


def _scan_args(target: str, profile: str, has_permission: bool, allow_public_target: bool = False, compact_logo: bool = False) -> Namespace:
    return Namespace(
        target=target,
        profile=profile,
        ports=None,
        timeout=1.0,
        concurrency=50,
        i_have_permission=has_permission,
        allow_public_target=allow_public_target,
        explain=False,
        ask_explain=False,
        compact_logo=compact_logo,
    )


def _choose_profile(default: str = "beginner") -> str:
    if not _confirm(f"Use the {default} profile?"):
        profiles = [profile for profile in list_profiles() if profile != "playground"]
        console.print("[dim]Profiles: " + ", ".join(profiles) + "[/]")
        selected = console.input("Profile: ").strip()
        if selected in profiles:
            return selected
        console.print(f"[#d7b56d]Using {default} profile.[/]")
    return default


def this_computer_scan(compact_logo: bool = False) -> int:
    has_permission = _confirm("Scan this computer now?")
    return run_authorized_scan(_scan_args("127.0.0.1", "beginner", has_permission, compact_logo=compact_logo))


def private_lab_scan(compact_logo: bool = False) -> int:
    console.print("[yellow]Use this only for a device you own or manage on your local network.[/]")
    target = console.input("Private IP or local hostname: ").strip()
    has_permission = _confirm("Do you own or have permission to scan this device?")
    profile = _choose_profile("beginner")
    return run_authorized_scan(_scan_args(target, profile, has_permission, compact_logo=compact_logo))


def authorized_website_scan(compact_logo: bool = False) -> int:
    console.print("[#d7b56d]Website/Public IP scans are supported for targets you own or have written permission to test.[/]")
    target = console.input("Domain or public IP: ").strip()
    console.print("[#d7b56d]Public targets can belong to other people. Only continue if you own this target or have written permission.[/]")
    token = console.input("Type AUTHORIZED to continue: ").strip()
    if token != "AUTHORIZED":
        console.print("[#d98b8b]Cancelled. Returning to the main menu.[/]")
        return 0
    return run_authorized_scan(_scan_args(target, "web", True, allow_public_target=True, compact_logo=compact_logo))


def _run_interactive_scan(args: Namespace, compact_logo: bool = False, profile_override: str | None = None, mode: str = "Authorized Scan") -> InteractiveResult:
    if getattr(args, "full_range", False):
        profile, ports = "full-range", FULL_RANGE_PORTS
        decision = evaluate_full_range_permission(args.target, args.i_have_permission)
    else:
        profile, ports = choose_ports(profile_override or getattr(args, "profile", None), getattr(args, "ports", None))
        decision = evaluate_scan_permission(args.target, args.i_have_permission, getattr(args, "allow_public_target", False))
    if not decision.allowed:
        title_header(compact_logo=compact_logo)
        console.print(f"[bold red]Scan refused:[/] {decision.reason}")
        return InteractiveResult(lambda: _run_interactive_scan(args, compact_logo, profile_override, mode), [])
    _, _, results = asyncio.run(
        _run_scan(
            args.target,
            profile,
            ports,
            args.timeout,
            args.concurrency,
            mode=mode,
            explain=False,
            ask_explain=False,
            compact_logo=compact_logo,
        )
    )
    return InteractiveResult(lambda: _run_interactive_scan(args, compact_logo, profile_override, mode), results)


def interactive_playground(compact_logo: bool = False) -> InteractiveResult:
    _, _, results = asyncio.run(_run_playground(1.0, 10, explain=False, ask_explain=False, compact_logo=compact_logo))
    return InteractiveResult(lambda: interactive_playground(compact_logo), results)


def interactive_this_computer(compact_logo: bool = False) -> InteractiveResult:
    has_permission = _confirm("Scan this computer now?")
    args = _scan_args("127.0.0.1", "beginner", has_permission, compact_logo=compact_logo)
    return _run_interactive_scan(args, compact_logo)


def interactive_private_lab(compact_logo: bool = False) -> InteractiveResult:
    console.print("[yellow]Use this only for a device you own or manage on your local network.[/]")
    target = console.input("Private IP or local hostname: ").strip()
    has_permission = _confirm("Do you own or have permission to scan this device?")
    profile = _choose_profile("beginner")
    args = _scan_args(target, profile, has_permission, compact_logo=compact_logo)
    return _run_interactive_scan(args, compact_logo)


def interactive_lab(compact_logo: bool = False) -> InteractiveResult:
    console.print("[#d7b56d]Metasploitable 2 should be isolated on a local lab network.[/]")
    target = console.input("Local Metasploitable 2 VM IP: ").strip()
    isolated = _confirm("Is this VM running in an isolated local lab network?")
    has_permission = _confirm("Do you have permission to scan this lab VM?")
    args = Namespace(
        target=target,
        profile="metasploitable2",
        ports=None,
        timeout=1.0,
        concurrency=50,
        i_have_permission=bool(isolated and has_permission),
        allow_public_target=False,
        explain=False,
        ask_explain=False,
        compact_logo=compact_logo,
    )
    return _run_interactive_scan(args, compact_logo, profile_override="metasploitable2", mode="Metasploitable 2 Lab")


def interactive_full_local(compact_logo: bool = False) -> InteractiveResult | None:
    console.print("[#d7b56d]Full Local Port Scan checks TCP ports 1-65535 on local/private targets only.[/]")
    target = console.input("Local/private target IP or hostname: ").strip()
    has_permission = _confirm("Do you own or have permission to scan this local/private target?")
    if not has_permission:
        console.print("[#d98b8b]Cancelled.[/]")
        return None
    args = Namespace(
        target=target,
        profile=None,
        ports=None,
        timeout=1.0,
        concurrency=25,
        i_have_permission=True,
        allow_public_target=False,
        explain=False,
        ask_explain=False,
        compact_logo=compact_logo,
        full_range=True,
    )
    return _run_interactive_scan(args, compact_logo, mode="Full Local Port Scan")


def interactive_website(compact_logo: bool = False) -> InteractiveResult | None:
    console.print("[#d7b56d]Website/Public IP scans are supported for targets you own or have written permission to test.[/]")
    target = console.input("Domain or public IP: ").strip()
    console.print("[#d7b56d]Public targets can belong to other people. Only continue if you own this target or have written permission.[/]")
    token = console.input("Type AUTHORIZED to continue: ").strip()
    if token != "AUTHORIZED":
        console.print("[#d98b8b]Cancelled.[/]")
        return None
    args = _scan_args(target, "web", True, allow_public_target=True, compact_logo=compact_logo)
    return _run_interactive_scan(args, compact_logo, mode="Website / Public IP")


def interactive_demo(compact_logo: bool = False) -> InteractiveResult:
    run_demo(compact_logo=compact_logo)
    return InteractiveResult(lambda: interactive_demo(compact_logo), [], rerun_label="generate demo again")


def interactive_metasploitable_demo(compact_logo: bool = False) -> InteractiveResult:
    run_metasploitable_demo(compact_logo=compact_logo)
    from .report import metasploitable_demo_results

    return InteractiveResult(lambda: interactive_metasploitable_demo(compact_logo), metasploitable_demo_results(), rerun_label="run tour again")


def interactive_learning_center(compact_logo: bool = False) -> InteractiveResult:
    run_learning_center(compact_logo=compact_logo)
    return InteractiveResult(lambda: interactive_learning_center(compact_logo), [], rerun_label="open learning center again")


def interactive_quiz(compact_logo: bool = False) -> InteractiveResult:
    run_quiz(compact_logo=compact_logo)
    return InteractiveResult(lambda: interactive_quiz(compact_logo), [], rerun_label="take quiz again")


def interactive_learning_quiz(compact_logo: bool = False) -> InteractiveResult:
    console.print("[#d7b56d]Port Knowledge[/]")
    console.print("[#d7b56d][1][/] Port Learning Center")
    console.print("[#d7b56d][2][/] Port Knowledge Quiz")
    choice = console.input("Select: ").strip()
    if choice == "1":
        return interactive_learning_center(compact_logo)
    return interactive_quiz(compact_logo)


def guided_scan() -> int:
    target = console.input("Target IP or hostname: ").strip()
    has_permission = _confirm("Do you have permission to scan this target?")
    allow_public = _confirm("If this target is public, do you own it or have written permission?")
    args = Namespace(
        target=target,
        profile="beginner",
        ports=None,
        timeout=1.0,
        concurrency=50,
        i_have_permission=has_permission,
        allow_public_target=allow_public,
        explain=False,
        ask_explain=False,
    )
    return run_authorized_scan(args)


def lab_scan(compact_logo: bool = False) -> int:
    console.print("[#d7b56d]Metasploitable 2 should be isolated on a local lab network.[/]")
    target = console.input("Local Metasploitable 2 VM IP: ").strip()
    isolated = _confirm("Is this VM running in an isolated local lab network?")
    has_permission = _confirm("Do you have permission to scan this lab VM?")
    args = Namespace(
        target=target,
        profile="metasploitable2",
        ports=None,
        timeout=1.0,
        concurrency=50,
        i_have_permission=bool(isolated and has_permission),
        allow_public_target=False,
        explain=False,
        ask_explain=True,
        compact_logo=compact_logo,
    )
    return run_authorized_scan(args, profile_override="metasploitable2")


def playground_scan(compact_logo: bool = False) -> int:
    args = Namespace(timeout=1.0, concurrency=10, explain=False, ask_explain=False, compact_logo=compact_logo)
    return run_playground(args)


def _open_results(results: list[ScanResult]) -> list[ScanResult]:
    return [result for result in results if result.status == "open"]


def _next_menu(result: InteractiveResult, no_clear: bool, compact_logo: bool) -> bool:
    current = result
    while True:
        has_notes = bool(_open_results(current.results))
        console.print()
        console.print("[#d7b56d]Next:[/]")
        if has_notes:
            console.print("[#d7b56d][L][/] learn about these ports")
        console.print("[#d7b56d][M][/] main menu")
        console.print(f"[#d7b56d][R][/] {current.rerun_label}")
        console.print("[#d7b56d][Q][/] quit")
        console.print()
        choice = console.input("Select: ").strip().lower()
        if choice == "":
            choice = "m"
        if choice == "n":
            console.print("[dim]Did you mean main menu? Returning to main menu.[/]")
            return True
        if choice == "l":
            if has_notes:
                learning_cards(current.results)
            else:
                console.print("[dim]No learning notes available.[/]")
            continue
        if choice == "m":
            return True
        if choice == "r":
            clear_screen(no_clear=no_clear)
            current = current.rerun()
            continue
        if choice == "q":
            return False
        console.print("[#d98b8b]Please choose L, M, R, or Q.[/]" if has_notes else "[#d98b8b]Please choose M, R, or Q.[/]")


def run_menu(no_clear: bool = False, compact_logo: bool = False) -> int:
    try:
        while True:
            clear_screen(no_clear=no_clear)
            title_header(compact_logo=compact_logo)
            console.print()
            console.print("[#d7b56d][1][/] Playground Tour             [dim]safe local practice, no VM needed[/]")
            console.print("[#d7b56d][2][/] Metasploitable Demo Tour    [dim]learn lab ports without installing a VM[/]")
            console.print("[#d7b56d][3][/] This Computer               [dim]scan localhost[/]")
            console.print("[#d7b56d][4][/] Private IP / Home Lab       [dim]scan a device you own[/]")
            console.print("[#d7b56d][5][/] Metasploitable 2 VM Scan    [dim]scan your isolated local VM[/]")
            console.print("[#d7b56d][6][/] Website / Public IP         [dim]supported with authorization[/]")
            console.print("[#d7b56d][7][/] Full Local Port Scan        [dim]1-65535 on local/private targets only[/]")
            console.print("[#d7b56d][8][/] Port Knowledge Quiz         [dim]20-question learning test[/]")
            console.print("[#d7b56d][9][/] Demo Report                 [dim]generate sample output[/]")
            console.print("[#d7b56d][0][/] Exit")
            console.print()
            choice = console.input("Select: ").strip()
            if choice == "0":
                console.print("Goodbye.")
                return 0

            clear_screen(no_clear=no_clear)
            result: InteractiveResult | None
            if choice == "1":
                result = interactive_playground(compact_logo)
            elif choice == "2":
                result = interactive_metasploitable_demo(compact_logo)
            elif choice == "3":
                result = interactive_this_computer(compact_logo)
            elif choice == "4":
                result = interactive_private_lab(compact_logo)
            elif choice == "5":
                result = interactive_lab(compact_logo)
            elif choice == "6":
                result = interactive_website(compact_logo)
            elif choice == "7":
                result = interactive_full_local(compact_logo)
            elif choice == "8":
                result = interactive_learning_quiz(compact_logo)
            elif choice == "9":
                result = interactive_demo(compact_logo)
            else:
                console.print("[#d98b8b]Please choose a listed number.[/]")
                continue
            if result is None:
                continue
            if not _next_menu(result, no_clear, compact_logo):
                return 0
    except KeyboardInterrupt:
        console.print("\nGoodbye.")
        return 0
