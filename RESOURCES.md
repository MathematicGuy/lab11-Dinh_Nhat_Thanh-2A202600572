# Guardrails, HITL, and Responsible AI Resources

## Knowledge

- [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
  Use for: the threat model behind this repo, especially prompt injection, insecure output handling, sensitive information disclosure, insecure plugin design, excessive agency, and overreliance.
- [OpenAI Cookbook: How to implement LLM guardrails](https://developers.openai.com/cookbook/examples/how_to_use_guardrails)
  Use for: practical guardrail patterns, tradeoffs between false positives and false negatives, and why lightweight checks should run in parallel to reduce latency.
- [OpenAI API Safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
  Use for: production safety posture, moderation layering, and when human review is appropriate.
- [NVIDIA NeMo Guardrails Developer Guide](https://docs.nvidia.com/nemo/guardrails/latest/home)
  Use for: programmable rails, especially input rails, output rails, topical rails, and dialog constraints.
- [Day-11 README](./README.md)
  Use for: the repo's intended learning objectives, file layout, and TODO mapping.
- [Assignment 11: Build a Production Defense-in-Depth Pipeline](./assignment11_defense_pipeline.md)
  Use for: the production framing, required safety layers, testing requirements, and report questions that define "good enough" for this project.

## Wisdom (Communities)

- [OWASP GenAI Security Project](https://genai.owasp.org/)
  Use for: current community guidance and practical discussion around LLM application security.
- [NVIDIA NeMo Guardrails GitHub Discussions](https://github.com/NVIDIA/NeMo-Guardrails)
  Use for: implementation details and real-world rail design questions when Colang behavior is unclear.

## Gaps

- There is no single repo-local document yet that explains how to balance safety and latency across input, model, output, and HITL from a red-team perspective. The lessons in this workspace will fill that gap.
