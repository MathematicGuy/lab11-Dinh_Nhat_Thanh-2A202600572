# Improvement Tracker

This file tracks the implementation progress for the Day-11 base code in `src/` so it is clear where the repo moved forward and what still needs deeper iteration later.

## Step 1: Adversarial attack coverage

- Completed the 5 manual adversarial prompts in `src/attacks/attacks.py`.
- Improved `run_attacks()` so attack results classify likely blocked vs leaked behavior using refusal and secret markers.
- Impact:
  - The attack phase now demonstrates realistic red-team patterns instead of placeholder prompts.
  - Before/after comparisons in the testing pipeline now have more useful signal.

## Step 2: Input guardrails

- Implemented regex-based prompt-injection detection in `src/guardrails/input_guardrails.py`.
- Implemented topic filtering using allowed and blocked topic lists.
- Implemented `InputGuardrailPlugin.on_user_message_callback()` with explicit block messages and counters.
- Impact:
  - Obvious jailbreaks, secret-extraction attempts, and off-topic traffic are now blocked before the LLM runs.
  - This reduces both safety risk and unnecessary model latency.

## Step 3: Output guardrails and LLM judge scaffolding

- Implemented `content_filter()` patterns for phone, email, ID, API key, password, and internal host leakage.
- Created the base `safety_judge_agent`.
- Implemented `OutputGuardrailPlugin.after_model_callback()` to redact sensitive output and optionally replace unsafe content with a safe refusal.
- Impact:
  - The repo now has a working post-generation safety layer instead of placeholders.
  - Sensitive output can be redacted even when unsafe content escapes earlier layers.

## Step 4: NeMo Guardrails coverage

- Added role-confusion, encoding-attack, and Vietnamese-injection Colang rules in `src/guardrails/nemo_guardrails.py`.
- Added matching test prompts for the new rules.
- Impact:
  - The NeMo section now demonstrates broader attack coverage beyond the original basic examples.

## Step 5: Security testing pipeline

- Wired the protected-agent comparison path in `src/testing/testing.py`.
- Implemented batch execution in `SecurityTestPipeline.run_all()`.
- Implemented metrics calculation for block rate, leak rate, and leaked secret aggregation.
- Impact:
  - Part 3 now has base comparison and reporting logic needed for the assignment evidence.

## Step 6: HITL routing

- Implemented `ConfidenceRouter.route()` in `src/hitl/hitl.py`.
- Replaced placeholder HITL decision points with real banking scenarios and reviewer context.
- Impact:
  - Part 4 now reflects an actual escalation design instead of a conceptual stub.
  - The repo can now teach the distinction between confidence-based routing and risk-based escalation.

## Step 7: Runtime verification and blockers

- Updated `src/core/config.py` so missing `GOOGLE_API_KEY` no longer crashes non-interactive runs with `EOFError`.
- Fixed `src/main.py` so full-run mode handles `parts=None` correctly.
- Installed `google-adk` into the active interpreter so the ADK-based modules can import and run.
- Verified runtime behavior:
  - Part 2 runs locally
  - Part 4 runs locally
  - Part 1 and Part 3 now skip cleanly when `GOOGLE_API_KEY` is not set
- Current blocker:
  - `nemoguardrails` is still not installed because one dependency (`annoy`) requires Microsoft C++ Build Tools on this machine.
- Impact:
  - The repo is now runnable offline for the non-live sections instead of failing immediately.
  - The remaining blocked functionality is environmental, not a base-code syntax issue.

## Step 8: Notebook completion

- Patched `notebooks/lab11_guardrails_hitl.ipynb` so the main TODO code cells now match the implemented `src` logic.
- Completed notebook sections for:
  - adversarial prompts
  - AI-generated attacks
  - injection detection
  - topic filtering
  - input guardrail plugin
  - content filter
  - LLM-as-judge setup
  - output guardrail plugin
  - NeMo Colang rules
  - protected attack rerun
  - automated security pipeline
  - confidence routing
  - HITL decision points
- Verified:
  - notebook JSON parses successfully
  - the original code-placeholder patterns targeted in the notebook are gone
- Impact:
  - The teaching notebook is now aligned with the base `src` implementation instead of diverging from it.
  - You can use the notebook as the main lab artifact without redoing the same TODOs by hand.

## Step 9: Provider fallback and notebook cleanup

- Added a live-provider fallback path in `src/core/config.py`:
  - prefer `GOOGLE_API_KEY`
  - fall back to `OPENROUTER_API_KEY`
- Wired ADK agents to use:
  - Google model string directly when Google is configured
  - `LiteLlm("openrouter/google/gemini-2.5-flash")` when OpenRouter is configured
- Updated AI-generated attack creation in `src/attacks/attacks.py` so it uses:
  - `google.genai` on Google
  - `OpenAI(base_url="https://openrouter.ai/api/v1")` on OpenRouter
- Mirrored the same fallback logic into `notebooks/lab11_guardrails_hitl.ipynb`.
- Cleaned the notebook security report section so it no longer contains raw blank placeholders.
- Important note:
  - the installed local LiteLLM catalog exposes OpenRouter `google/gemini-2.5-flash`, not `gemini-2.5-flash-lite`, so the fallback uses the closest available Gemini 2.5 Flash route.
- Impact:
  - The repo and notebook are no longer hard-wired to Google-only credentials.
  - You can run live sections with either Google or OpenRouter, with NeMo still remaining Google-only in the notebook configuration.

## What still needs future improvement

- Add dedicated automated tests under a `tests/` directory instead of relying mainly on inline demo functions.
- Validate the ADK callback behavior against live runtime responses, especially output mutation and judge behavior.
- Add rate limiting, audit logging, and monitoring helpers to fully satisfy the production assignment extension.
- Tighten `run_attacks()` blocked/leaked classification once real protected-agent outputs are observed.
- Install a working NeMo dependency stack or use a Python environment that already has the required native build support.
