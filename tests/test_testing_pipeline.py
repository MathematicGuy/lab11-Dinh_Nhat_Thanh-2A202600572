import asyncio

from testing.testing import SecurityTestPipeline, TestResult


def test_security_pipeline_detects_known_secret_leaks():
    pipeline = SecurityTestPipeline(agent=None, runner=None)

    assert pipeline._check_for_leaks("The password is admin123.") == ["admin123"]
    assert pipeline._check_for_leaks("Nothing sensitive here.") == []


def test_security_pipeline_calculates_metrics():
    pipeline = SecurityTestPipeline(agent=None, runner=None)
    results = [
        TestResult(1, "A", "q1", "safe", True, []),
        TestResult(2, "B", "q2", "leak", False, ["admin123"]),
    ]

    metrics = pipeline.calculate_metrics(results)

    assert metrics["total"] == 2
    assert metrics["blocked"] == 1
    assert metrics["leaked"] == 1
    assert metrics["block_rate"] == 0.5
    assert metrics["leak_rate"] == 0.5


def test_security_pipeline_run_single_marks_leaks(monkeypatch):
    pipeline = SecurityTestPipeline(agent=object(), runner=object())

    async def fake_chat_with_agent(agent, runner, user_message):
        return "The admin password is admin123.", None

    monkeypatch.setattr("testing.testing.chat_with_agent", fake_chat_with_agent)

    result = asyncio.run(
        pipeline.run_single({"id": 7, "category": "Leak", "input": "prompt"})
    )

    assert result.attack_id == 7
    assert result.blocked is False
    assert result.leaked_secrets == ["admin123"]
