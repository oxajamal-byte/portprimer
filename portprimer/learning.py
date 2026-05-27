from __future__ import annotations

from .ui import console, title_header


LESSONS: dict[str, list[str]] = {
    "What is a port?": [
        "A port is a numbered place where network traffic can arrive.",
        "Programs listen on ports so clients know where to connect.",
        "A port is a clue about what a system might be doing.",
    ],
    "TCP vs UDP": [
        "TCP makes a connection before data moves.",
        "UDP sends messages without a connection handshake.",
        "PortPrimer teaches TCP connect scanning only.",
    ],
    "What does open mean?": [
        "Open usually means a service accepted a connection.",
        "Closed means nothing accepted the connection on that port.",
        "Timeout means no clear answer came back in time.",
    ],
    "Open is not vulnerable": [
        "An open port is not automatically a vulnerability.",
        "It is a clue to identify, understand, and scope.",
        "Exposure, configuration, auth, and need all matter.",
    ],
    "Common port families": [
        "Web: 80, 443, 8080, 8443.",
        "Admin: 22, 3389, 5900.",
        "Data and files: 3306, 5432, 445, 2049.",
    ],
    "Safe thinking": [
        "Scan only systems you own or have permission to test.",
        "Keep admin and data services private when possible.",
        "Learn what owns a port before changing anything.",
    ],
}


def run_learning_center(compact_logo: bool = False) -> int:
    title_header(compact_logo=compact_logo)
    console.print()
    console.print("[#d7b56d]Port Learning Center[/]")
    for title, lines in LESSONS.items():
        console.print()
        console.print(f"[#f3ead7]{title}[/]")
        for line in lines:
            console.print(f"  [dim]{line}[/]")
    return 0
