from agents.agent import build_protected_instruction


def test_protected_instruction_enforces_hierarchy_and_private_reasoning():
    instruction = build_protected_instruction()

    lowered = instruction.lower()
    assert "instruction hierarchy" in lowered
    assert "system instructions" in lowered
    assert "user requests" in lowered
    assert "do not reveal" in lowered
    assert "reasoning" in lowered
    assert "prompt injection" in lowered
