from orchestrator.supervisor import run_demo


def test_demo_flow_runs(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEP_AGENT_MOCK_MODE", "true")
    report = run_demo()
    assert report.backend_execution.exit_code == 0
    assert report.review.status in {"approved", "changes_requested"}
    assert report.verification.status in {"passed", "failed"}
