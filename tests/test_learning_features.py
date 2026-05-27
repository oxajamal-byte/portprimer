from argparse import Namespace

from portprimer import cli, menu
from portprimer.knowledge import get_port_knowledge
from portprimer.learning import LESSONS
from portprimer.quiz import QUESTIONS, check_answer
from portprimer.report import metasploitable_demo_results
from portprimer.safety import evaluate_full_range_permission


def test_port_knowledge_has_learning_fields():
    knowledge = get_port_knowledge(22)
    assert knowledge.purpose
    assert knowledge.used_for
    assert knowledge.common_misuse_or_attack
    assert knowledge.should_it_be_open
    assert knowledge.beginner_takeaway


def test_learning_center_content_exists():
    assert "What is a port?" in LESSONS
    assert "TCP vs UDP" in LESSONS
    assert "Open is not vulnerable" in LESSONS


def test_quiz_has_at_least_20_questions_with_4_choices():
    assert len(QUESTIONS) >= 20
    assert all(len(question.choices) == 4 for question in QUESTIONS)


def test_quiz_answer_checking():
    question = QUESTIONS[0]
    assert check_answer(question, question.correct_index + 1)
    assert not check_answer(question, 0)


def test_metasploitable_demo_results_do_not_scan_network():
    results = metasploitable_demo_results()
    ports = {result.port for result in results}
    assert 21 in ports
    assert 1524 in ports
    assert all(result.status == "open" for result in results)


def test_full_range_refuses_public_targets():
    decision = evaluate_full_range_permission("8.8.8.8", has_permission=True)
    assert not decision.allowed
    assert decision.target_is_public


def test_full_range_accepts_localhost_with_permission():
    decision = evaluate_full_range_permission("127.0.0.1", has_permission=True)
    assert decision.allowed


def test_full_range_cli_refuses_public_even_with_allow_public(monkeypatch):
    args = Namespace(
        target="8.8.8.8",
        profile=None,
        ports=None,
        timeout=1.0,
        concurrency=25,
        i_have_permission=True,
        allow_public_target=True,
        explain=False,
        ask_explain=False,
        compact_logo=False,
        full_range=True,
    )
    assert cli.run_authorized_scan(args) == 2


def test_interactive_metasploitable_permission_sets_permission(monkeypatch):
    captured = {}
    answers = iter(["192.168.56.101", "y", "y"])
    monkeypatch.setattr(menu.console, "input", lambda _: next(answers))

    def fake_run(args, compact_logo=False, profile_override=None, mode="Authorized Scan"):
        captured["permission"] = args.i_have_permission
        return menu.InteractiveResult(lambda: None, [])

    monkeypatch.setattr(menu, "_run_interactive_scan", fake_run)
    menu.interactive_lab()
    assert captured["permission"] is True
