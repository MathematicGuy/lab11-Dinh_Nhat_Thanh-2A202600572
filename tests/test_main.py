import asyncio

import main


def test_part2_guardrails_skips_nemo_and_runs_local_checks(monkeypatch, capsys):
    monkeypatch.setattr("guardrails.nemo_guardrails.NEMO_AVAILABLE", False)
    calls = []

    monkeypatch.setattr(
        "guardrails.input_guardrails.test_injection_detection",
        lambda: calls.append("input-detect"),
    )
    monkeypatch.setattr(
        "guardrails.input_guardrails.test_topic_filter",
        lambda: calls.append("topic-filter"),
    )

    async def fake_input_plugin_test():
        calls.append("input-plugin")

    monkeypatch.setattr(
        "guardrails.input_guardrails.test_input_plugin",
        fake_input_plugin_test,
    )
    monkeypatch.setattr(
        "guardrails.output_guardrails._init_judge",
        lambda: calls.append("judge-init"),
    )
    monkeypatch.setattr(
        "guardrails.output_guardrails.test_content_filter",
        lambda: calls.append("content-filter"),
    )

    asyncio.run(main.part2_guardrails())
    output = capsys.readouterr().out

    assert calls == [
        "input-detect",
        "topic-filter",
        "input-plugin",
        "judge-init",
        "content-filter",
    ]
    assert "Skipping Part 2C" in output


def test_main_continues_when_live_part_fails(monkeypatch, capsys):
    async def failing_part1():
        raise RuntimeError("provider failure")

    monkeypatch.setattr(main, "part1_attacks", failing_part1)
    monkeypatch.setattr(main, "part2_guardrails", lambda: None)
    monkeypatch.setattr(main, "part3_testing", lambda: None)
    monkeypatch.setattr(main, "part4_hitl", lambda: None)
    monkeypatch.setattr(main, "setup_api_key", lambda: True)

    asyncio.run(main.main(parts=[1]))
    output = capsys.readouterr().out

    assert "Skipping Part 1 after runtime error: provider failure" in output
