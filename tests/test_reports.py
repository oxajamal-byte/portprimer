import json
import re

from portprimer.report import IMPORTANT_REPORT_WORDING, PLAYGROUND_REPORT_WORDING, build_report_markdown, generate_demo_report, write_reports
from portprimer.scanner import ScanResult


def test_report_generation_basics(tmp_path):
    results = [ScanResult(22, "open"), ScanResult(80, "closed")]
    markdown_path, json_path = write_reports("127.0.0.1", "beginner", results, 1.0, 10, reports_dir=tmp_path)

    markdown = markdown_path.read_text(encoding="utf-8")
    data = json.loads(json_path.read_text(encoding="utf-8"))

    assert "# PortPrimer Report" in markdown
    assert IMPORTANT_REPORT_WORDING in markdown
    assert "| 22 | SSH | Admin Door | Keep private |" in markdown
    assert data["summary"]["open"] == 1
    assert data["open_services"][0]["service"] == "SSH"
    assert re.match(r"portprimer-scan-beginner-127-0-0-1-\d{8}-\d{4}\.md", markdown_path.name)
    assert re.match(r"portprimer-scan-beginner-127-0-0-1-\d{8}-\d{4}\.json", json_path.name)


def test_demo_mode_report_generation(tmp_path):
    markdown_path, json_path = generate_demo_report(reports_dir=tmp_path)
    assert markdown_path.exists()
    assert json_path.exists()
    assert re.match(r"portprimer-demo-local-lab-\d{8}-\d{4}\.md", markdown_path.name)


def test_playground_report_generation(tmp_path):
    results = [
        ScanResult(8022, "open"),
        ScanResult(8080, "open"),
        ScanResult(15432, "open"),
        ScanResult(16379, "open"),
        ScanResult(18080, "open"),
    ]
    markdown_path, json_path = write_reports("127.0.0.1", "playground", results, 1.0, 10, reports_dir=tmp_path)
    markdown = markdown_path.read_text(encoding="utf-8")
    data = json.loads(json_path.read_text(encoding="utf-8"))

    assert PLAYGROUND_REPORT_WORDING in markdown
    assert data["profile"] == "playground"
    assert data["playground_note"] == PLAYGROUND_REPORT_WORDING
    assert data["summary"]["open"] == 5
    assert re.match(r"portprimer-playground-127-0-0-1-\d{8}-\d{4}\.md", markdown_path.name)


def test_report_handles_unknown_open_port():
    markdown = build_report_markdown("lab", "custom", [ScanResult(65000, "open")], 1.0, 5)
    assert "Unknown Door" in markdown
    assert "Learn more before changing" in markdown


def test_report_no_open_services_uses_message_not_fake_row():
    markdown = build_report_markdown("lab", "custom", [ScanResult(80, "closed")], 1.0, 5)
    assert "No open services found in this scan set." in markdown
    assert "| None |" not in markdown
    assert "| - |" not in markdown
