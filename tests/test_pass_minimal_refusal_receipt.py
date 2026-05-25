"""Test: PASS on a complete minimal refusal-receipt proof pack."""
from src.artifact_readiness_engine.inspector import inspect_file

PASS_FILE = "examples/pass/minimal-refusal-receipt.json"


def test_pass_status():
    result = inspect_file(PASS_FILE)
    assert result["status"] == "PASS", (
        f"Expected PASS, got {result['status']}.\nIssues: {result['issues']}"
    )


def test_pass_no_issues():
    result = inspect_file(PASS_FILE)
    assert not result["issues"], f"Expected no issues, got: {result['issues']}"


def test_pass_all_surfaces():
    result = inspect_file(PASS_FILE)
    for surface, detail in result["scores"].items():
        assert detail["result"] == "PASS", f"{surface} did not PASS: {detail}"
