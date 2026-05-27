from __future__ import annotations

import random
from dataclasses import dataclass

from .ui import console, title_header


@dataclass(frozen=True)
class QuizQuestion:
    prompt: str
    choices: tuple[str, str, str, str]
    correct_index: int
    explanation: str
    category: str


QUESTIONS: list[QuizQuestion] = [
    QuizQuestion("Which port is commonly used for HTTPS?", ("22", "80", "443", "3306"), 2, "HTTPS usually uses 443 for encrypted web traffic.", "web ports"),
    QuizQuestion("Which port is commonly used for SSH?", ("21", "22", "25", "110"), 1, "SSH commonly uses 22 for remote administration.", "admin ports"),
    QuizQuestion("What does an open port usually mean?", ("A service answered", "The host is vulnerable", "A password is weak", "The OS is known"), 0, "Open means a service accepted the connection attempt.", "meaning of open ports"),
    QuizQuestion("Which service is commonly associated with port 3306?", ("PostgreSQL", "MySQL", "SMTP", "DNS"), 1, "MySQL commonly listens on 3306.", "database ports"),
    QuizQuestion("Which service is commonly associated with port 5432?", ("PostgreSQL", "Redis", "FTP", "RDP"), 0, "PostgreSQL commonly listens on 5432.", "database ports"),
    QuizQuestion("Which port is commonly used for HTTP?", ("23", "53", "80", "139"), 2, "HTTP commonly uses 80.", "web ports"),
    QuizQuestion("Which port is commonly used for DNS?", ("25", "53", "111", "445"), 1, "DNS commonly uses 53.", "system ports"),
    QuizQuestion("Which port is commonly used for SMTP?", ("25", "110", "143", "993"), 0, "SMTP commonly uses 25 for mail transfer.", "mail ports"),
    QuizQuestion("Which port is commonly used for SMB file sharing?", ("139", "445", "5900", "6379"), 1, "SMB commonly uses 445.", "file sharing"),
    QuizQuestion("Which service is legacy remote login?", ("Telnet", "HTTPS", "PostgreSQL", "NTP"), 0, "Telnet is a legacy remote login protocol.", "legacy services"),
    QuizQuestion("Which choice is safest for public targets?", ("Scan random sites", "Scan only with permission", "Try every port always", "Guess services"), 1, "Public targets need ownership or written permission.", "safe scanning ethics"),
    QuizQuestion("What is Metasploitable 2 for?", ("Public deployment", "Learning in an isolated lab", "Production hosting", "Email delivery"), 1, "Metasploitable 2 is intentionally vulnerable and belongs in isolated labs.", "Metasploitable/lab safety"),
    QuizQuestion("Which is true about open ports?", ("Always exploitable", "Always safe", "A clue to investigate", "Proof of malware"), 2, "An open port is a clue, not proof of vulnerability.", "meaning of open ports"),
    QuizQuestion("Where should admin ports usually be reachable?", ("Trusted networks", "All public networks", "Random scanners", "Anyone"), 0, "Admin access should be restricted to trusted users and networks.", "private vs public exposure"),
    QuizQuestion("Which port is commonly used for RDP?", ("22", "3389", "8080", "27017"), 1, "RDP commonly uses 3389.", "admin ports"),
    QuizQuestion("Which port is commonly used for Redis?", ("6379", "6667", "8180", "1524"), 0, "Redis commonly uses 6379.", "database ports"),
    QuizQuestion("Which is a mail retrieval protocol?", ("POP3", "SMB", "NFS", "IRC"), 0, "POP3 is used by mail clients to retrieve email.", "mail ports"),
    QuizQuestion("Which is a common web alternate port?", ("8080", "23", "512", "514"), 0, "8080 often hosts alternate web apps or proxies.", "web ports"),
    QuizQuestion("What should you do with an unknown open port?", ("Ignore it", "Assume it is safe", "Identify what owns it", "Assume it is critical"), 2, "Identify the owner and purpose before changing anything.", "safe scanning ethics"),
    QuizQuestion("Which port is common for VNC?", ("5900", "25", "53", "443"), 0, "VNC commonly uses 5900 for remote desktop access.", "admin ports"),
]


def check_answer(question: QuizQuestion, answer_number: int) -> bool:
    return answer_number - 1 == question.correct_index


def run_quiz(compact_logo: bool = False, count: int = 20) -> int:
    title_header(compact_logo=compact_logo)
    console.print()
    console.print("[#d7b56d]Port Knowledge Quiz[/]")
    selected = random.sample(QUESTIONS, k=min(count, len(QUESTIONS)))
    correct = 0
    missed: dict[str, int] = {}
    for index, question in enumerate(selected, start=1):
        console.print()
        console.print(f"[#f3ead7]{index}. {question.prompt}[/]")
        for choice_index, choice in enumerate(question.choices, start=1):
            console.print(f"  {choice_index}. {choice}")
        raw = console.input("Answer: ").strip()
        try:
            answer = int(raw)
        except ValueError:
            answer = 0
        if check_answer(question, answer):
            correct += 1
            console.print("[green]Correct.[/]")
        else:
            missed[question.category] = missed.get(question.category, 0) + 1
            console.print(f"[#d98b8b]Not quite.[/] Correct: {question.correct_index + 1}")
        console.print(f"[dim]{question.explanation}[/]")

    percent = round((correct / len(selected)) * 100)
    console.print()
    console.print(f"[#d7b56d]Score:[/] {correct}/{len(selected)}")
    console.print(f"[#d7b56d]Percentage:[/] {percent}%")
    if missed:
        topics = ", ".join(sorted(missed, key=missed.get, reverse=True)[:3])
        console.print(f"[#d7b56d]Review:[/] {topics}")
    else:
        console.print("[green]Strong fundamentals. Keep practicing safely.[/]")
    return 0
