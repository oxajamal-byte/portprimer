from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .knowledge import get_port_knowledge
from .scanner import ScanResult
from .utils import ensure_reports_dir, filename_timestamp, safe_target_name, utc_timestamp

IMPORTANT_REPORT_WORDING = (
    "An open port is not automatically a vulnerability. It is a clue. Whether it matters "
    "depends on exposure, configuration, authentication, patching, and whether the service is needed."
)

PLAYGROUND_REPORT_WORDING = (
    "Playground Tour uses safe local practice services created by PortPrimer. They are not real vulnerable "
    "services, do not implement real protocols, and bind only to 127.0.0.1 so learners can see how open ports "
    "appear in a scan."
)


def summarize_results(results: list[ScanResult]) -> dict[str, int]:
    return {
        "open": sum(1 for result in results if result.status == "open"),
        "closed": sum(1 for result in results if result.status == "closed"),
        "timeout": sum(1 for result in results if result.status == "timeout"),
        "total": len(results),
    }


def build_report_markdown(target: str, profile: str, results: list[ScanResult], timeout: float, concurrency: int) -> str:
    summary = summarize_results(results)
    open_results = [result for result in results if result.status == "open"]
    lines = [
        "# PortPrimer Report",
        "",
        "## Target and scan settings",
        "",
        f"- Target: `{target}`",
        f"- Profile: `{profile}`",
        f"- Timeout: `{timeout}` seconds",
        f"- Concurrency: `{concurrency}`",
        f"- Generated: `{utc_timestamp()}`",
        "",
        "## Summary",
        "",
        IMPORTANT_REPORT_WORDING,
        "",
        *(["", PLAYGROUND_REPORT_WORDING, ""] if profile == "playground" else []),
        f"- Open ports: {summary['open']}",
        f"- Closed ports: {summary['closed']}",
        f"- Timed out ports: {summary['timeout']}",
        f"- Total checked: {summary['total']}",
        "",
    ]
    if open_results:
        lines.extend([
            "## Open services table",
            "",
            "| Port | Service | Door Type | Action Hint |",
            "| --- | --- | --- | --- |",
        ])
        for result in open_results:
            knowledge = get_port_knowledge(result.port)
            lines.append(f"| {result.port} | {knowledge.service} | {knowledge.learning_label} | {knowledge.action_hint} |")
    else:
        lines.extend(["## Open services", "", "No open services found in this scan set."])

    lines.extend(["", "## Beginner notes for each open service", ""])
    if open_results:
        for result in open_results:
            knowledge = get_port_knowledge(result.port)
            lines.extend([
                f"### {result.port}/tcp {knowledge.service}",
                "",
                f"- What it is: {knowledge.what_it_is}",
                f"- Used for: {knowledge.used_for}",
                f"- Why it matters: {knowledge.why_it_matters}",
                f"- What to watch: {knowledge.common_misuse_or_attack}",
                f"- Should it be open: {knowledge.should_it_be_open}",
                f"- Beginner note: {knowledge.beginner_note}",
                "",
            ])
    else:
        lines.extend(["No open services found in this scan set.", ""])

    lines.extend([
        "## Suggested next steps",
        "",
        "- Confirm each open service is expected for this system.",
        "- Keep admin, data, and private services reachable only by trusted users and networks.",
        "- Remove or disable services that are not needed.",
        "- Learn what owns an unknown port before changing it.",
        "",
        "## Responsible-use reminder",
        "",
        "Use PortPrimer only on systems you own, manage, or have clear permission to test. Do not scan random public targets.",
        "",
        "## Limitations",
        "",
        "PortPrimer performs normal TCP connect scanning only. It does not exploit services, test credentials, prove vulnerabilities, prove safety, fingerprint operating systems, grab aggressive banners, scan CIDR ranges, or replace Nmap.",
        "",
    ])
    return "\n".join(lines)


def build_results_json(target: str, profile: str, results: list[ScanResult], timeout: float, concurrency: int) -> dict[str, object]:
    open_items = []
    for result in results:
        if result.status == "open":
            knowledge = get_port_knowledge(result.port)
            open_items.append({"port": result.port, **asdict(knowledge)})
    payload: dict[str, object] = {
        "tool": "PortPrimer",
        "target": target,
        "profile": profile,
        "generated_at": utc_timestamp(),
        "settings": {"timeout": timeout, "concurrency": concurrency},
        "summary": summarize_results(results),
        "results": [asdict(result) for result in results],
        "open_services": open_items,
        "important_note": IMPORTANT_REPORT_WORDING,
    }
    if profile == "playground":
        payload["playground_note"] = PLAYGROUND_REPORT_WORDING
    return payload


def write_reports(
    target: str,
    profile: str,
    results: list[ScanResult],
    timeout: float,
    concurrency: int,
    reports_dir: Path = Path("reports"),
) -> tuple[Path, Path]:
    output_dir = ensure_reports_dir(reports_dir)
    name = safe_target_name(target)
    stamp = filename_timestamp()
    if profile == "demo":
        prefix = "demo"
        filename_target = name.removeprefix("demo-")
    elif profile == "playground":
        prefix = "playground"
        filename_target = name
    elif profile == "metasploitable-demo":
        prefix = "metasploitable-demo"
        filename_target = name.removeprefix("metasploitable-demo-")
    else:
        prefix = f"scan-{profile}"
        filename_target = name
    stem = f"portprimer-{prefix}-{filename_target}-{stamp}"
    markdown_path = output_dir / f"{stem}.md"
    json_path = output_dir / f"{stem}.json"
    markdown_path.write_text(build_report_markdown(target, profile, results, timeout, concurrency), encoding="utf-8")
    json_path.write_text(json.dumps(build_results_json(target, profile, results, timeout, concurrency), indent=2), encoding="utf-8")
    return markdown_path, json_path


def demo_results() -> list[ScanResult]:
    return [
        ScanResult(22, "open"),
        ScanResult(80, "open"),
        ScanResult(443, "closed"),
        ScanResult(3306, "closed"),
        ScanResult(8080, "open"),
    ]


def generate_demo_report(reports_dir: Path = Path("reports")) -> tuple[Path, Path]:
    return write_reports("demo-local-lab", "demo", demo_results(), timeout=1.0, concurrency=10, reports_dir=reports_dir)


METASPLOITABLE_DEMO_PORTS = [21, 22, 23, 25, 53, 80, 111, 139, 445, 512, 513, 514, 1099, 1524, 2049, 2121, 3306, 5432, 5900, 6667, 8180]


def metasploitable_demo_results() -> list[ScanResult]:
    return [ScanResult(port, "open") for port in METASPLOITABLE_DEMO_PORTS]


def generate_metasploitable_demo_report(reports_dir: Path = Path("reports")) -> tuple[Path, Path]:
    return write_reports("metasploitable-demo-tour", "metasploitable-demo", metasploitable_demo_results(), timeout=0.0, concurrency=0, reports_dir=reports_dir)
