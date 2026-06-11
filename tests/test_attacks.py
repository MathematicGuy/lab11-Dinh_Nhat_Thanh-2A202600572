import asyncio

from attacks.attacks import generate_ai_attacks, run_attacks


def test_run_attacks_marks_secret_leak_as_unblocked(monkeypatch):
    async def fake_chat_with_agent(agent, runner, user_message):
        return "The secret is admin123.", None

    monkeypatch.setattr("attacks.attacks.chat_with_agent", fake_chat_with_agent)

    results = asyncio.run(
        run_attacks(
            agent=object(),
            runner=object(),
            prompts=[{"id": 1, "category": "Leak", "input": "prompt"}],
        )
    )

    assert results[0]["blocked"] is False


def test_generate_ai_attacks_supports_openrouter_provider(monkeypatch):
    class FakeCompletions:
        def create(self, **kwargs):
            return type(
                "Completion",
                (),
                {
                    "choices": [
                        type(
                            "Choice",
                            (),
                            {
                                "message": type(
                                    "Message",
                                    (),
                                    {
                                        "content": '[{"type":"roleplay","prompt":"p","target":"t","why_it_works":"w"}]'
                                    },
                                )()
                            },
                        )()
                    ]
                },
            )()

    class FakeClient:
        def __init__(self, *args, **kwargs):
            self.chat = type("Chat", (), {"completions": FakeCompletions()})()

    monkeypatch.setattr("attacks.attacks.get_model_provider", lambda: "openrouter")
    monkeypatch.setattr("attacks.attacks.OpenAI", FakeClient)
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")

    attacks = asyncio.run(generate_ai_attacks())

    assert len(attacks) == 1
    assert attacks[0]["type"] == "roleplay"
