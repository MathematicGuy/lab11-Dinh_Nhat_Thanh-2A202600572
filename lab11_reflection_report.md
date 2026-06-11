# Summary & Reflection Report: Lab 11 — Guardrails & HITL
**Jupyter Notebook:** [lab11_guardrails_hitl.ipynb](file:///D:/Personlich/AIO/AIO2025%20-%20Main/_2026_Research/VIN%20Practitioner/Day-11-Guardrails-HITL-Responsible-AI/notebooks/lab11_guardrails_hitl.ipynb)  

---

## Summary & Reflection

### What you built:
1. **Attacked an unprotected agent:** Explored manual adversarial prompts (e.g., translation, completion, authority roleplay) to understand prompt injection vulnerabilities and the risk of exposing internal credentials (admin password, API key, database host).
2. **Used AI to generate attack test cases:** Implemented automated red teaming using an LLM to generate creative, long, and complex adversarial prompts across multiple categories.
3. **Implemented input guardrails:** Built injection detection (using regex matching for common attack phrases) and a topic filter (using allowed/blocked list checks) to block dangerous or off-topic inputs before they hit the LLM.
4. **Implemented output guardrails:** Built content filters (regex-based secret detectors) and integrated an LLM-as-Judge to intercept and redact leaked PII or secrets (like passwords, keys, phone numbers, and emails).
5. **Used NeMo Guardrails with Colang:** Defined declarative guardrail flows and intents (using Colang configs) to control the dialog structure and automatically handle off-topic chat, role-confusion, encoding, and language-specific injection attacks.
6. **Built an automated security testing pipeline:** Created a `SecurityTestPipeline` runner that runs batch tests, logs actions, tracks metrics, and generates a structured safety report.
7. **Compared before/after:** Evaluated the performance of the unprotected agent against the protected agent, measuring the exact improvement in blocked attacks.
8. **Designed HITL workflow with confidence routing:** Designed a `ConfidenceRouter` and created structured human-in-the-loop decision points mapping out trigger conditions, models (human-in-the-loop, human-on-the-loop, human-as-tiebreaker), and context for high-risk actions.

---

### Reflection questions:

#### 1. Which guardrail was most effective? Which needs improvement?
* **Most Effective:** **Output Guardrails (Content Redaction / Secret Detection)**. This is because output redaction is deterministic and acts as the final "fail-safe". Even if an attacker successfully injects instructions and tricks the model, the output filter prevents sensitive tokens (like `admin123` or `sk-vinbank-secret-2024`) from actually being sent back to the user.
* **Needs Improvement:** **Input Regex-based Guardrails**. Regular expressions are highly brittle. Attackers can easily bypass regex patterns using synonym swaps, character splitting (e.g., `p a s s w o r d`), homoglyphs (lookalike characters from other alphabets), or encoding tricks.

#### 2. Compare ADK Plugin vs NeMo Guardrails — pros/cons?
* **ADK Plugin (Google ADK)**:
  - *Pros:* Fully native to the runner framework; written in clean, familiar Python; very fast and predictable execution time; easy to integrate with custom databases or APIs.
  - *Cons:* Procedural implementation can lead to complex conditional logic as safety rules scale.
* **NeMo Guardrails (NVIDIA)**:
  - *Pros:* Highly declarative syntax (Colang) for writing conversational rules; manages state and dialog flows natively; separates application logic from safety configurations.
  - *Cons:* Higher setup complexity; introduces additional latency from internal LLM calls (e.g., classifying intents); has versioning and dependency conflicts with some python environments.

#### 3. Did AI-generated attacks find vulnerabilities you didn't think of?
* **Yes.** The AI-generated attacks combined multiple sophisticated vectors. For instance, rather than asking for the password directly, they used **context manipulation** (wrapping the request in a compliance auditing roleplay with fake ticket numbers) and **encoding requests** (asking for ROT13 or YAML formatting) which easily bypass simple keyword blocks but are understood by the core model.

#### 4. How much does HITL improve safety? What's the trade-off (latency, cost)?
* **Improvement:** Human-in-the-Loop (HITL) increases safety to near 100% for high-risk operations (e.g., transfers over $50,000 or account closures) because human oversight validates the context and user intent.
* **Trade-off:** Introducing humans creates massive **latency** (responses take minutes/hours rather than milliseconds) and high **operational cost** (paying human reviewers). Thus, HITL must be reserved only for high-value or highly ambiguous requests.

#### 5. In production, which framework would you use (NeMo, Guardrails AI, custom)? Why?
* I would recommend a **Hybrid Custom + NeMo approach**:
  - Use a **custom fast regex/keyword engine** for low-latency input blocking (rejecting obvious spam, SQL injections, and rate limits).
  - Use **NeMo Guardrails** for managing acceptable conversational dialog flows and redirecting off-topic conversations back to banking.
  - Use **custom regex/PII checkers** for output redaction as they are extremely fast and guaranteed to catch known secrets without the latency of an LLM call.

---

### Key Takeaways:
* **Guardrails are mandatory**, not optional. An unprotected agent will leak sensitive information with minimal prompting.
* **Defense in depth:** Combine input checks, output checkers, NeMo conversational flows, and HITL. No single layer catches everything.
* **HITL is a feature**, not a failure. It is the only way to manage high-value transactions safely.
* **Automate testing:** Red team your agents using automated AI prompts and pipelines before deploying to catch 80% of security vulnerabilities.
* **NeMo Guardrails** allows teams to define safety rules declaratively, separating policy from application logic.
* **Red team before you deploy:** Finding vulnerabilities early prevents real-world reputational and financial damage.
