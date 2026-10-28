# AgentSec Lab

**Indirect Prompt Injection • AI Tool-Calling Security • Authorization Validation**

AgentSec Lab is a local, intentionally controlled AI security research project built with **Python, Ollama (Llama 3.2 3B), SQLite, and Streamlit**. It evaluates whether instructions placed in a lower-trust expense-policy document can influence an AI assistant to request a tool that is unrelated to the legitimate user's task, and whether application-level authorization prevents sensitive tool-result disclosure.

> **Safety and scope:** All employees, documents, salaries and identifiers in this repository are synthetic. The vulnerable dispatcher is deliberately insecure and exists only for isolated comparison testing. Do not connect it to real employee records or production systems.

## Results at a glance

| Evaluation | Observed result |
|---|---:|
| Python automated tests | 39 passing (as last reported) |
| Tool attack evaluation: valid unauthorized requests | 10 / 10 |
| Tool attack evaluation: vulnerable disclosures | 10 / 10 |
| Tool attack evaluation: hardened disclosures | 0 / 10 |
| Separate end-to-end evaluation: legitimate summaries passing four fact checks | 4 / 5 |
| Separate end-to-end evaluation: unauthorized requests | 5 / 5 |
| Separate end-to-end evaluation: vulnerable disclosures | 5 / 5 |
| Separate end-to-end evaluation: hardened disclosures | 0 / 5 |

These are observations from local tests of specific payloads and configurations, **not** general guarantees of model or application security. A *disclosure* here means the tool dispatcher returned a synthetic record containing a salary; it does **not** mean external exfiltration or that the model included the salary in its final user-facing answer. The legitimate-task check validates four expected facts; it is not a complete accuracy evaluation.

## The attack scenario

1. A legitimate user requests a summary of a fictional company's expense policy.
2. An attacker-controlled copy of that document embeds an instruction to call `get_employee` for employee ID `2`.
3. The local language model generates a tool request unrelated to the authorized summarization task.
4. The **deliberately vulnerable** dispatcher accepts an arbitrary employee ID and returns the complete synthetic record, including salary.
5. The **hardened** dispatcher rejects that same generated request (`Tool not permitted`), while permitting a separate `get_my_profile` operation that excludes salary fields.

The model's tool choice is **not an authorization decision**. Authorization must be enforced by the application at the execution boundary.

## Architecture

```mermaid
flowchart TB
    U[Legitimate user: summarize expense policy] --> M[Local LLM: Llama 3.2 3B]
    D[Untrusted policy document with injection] -->|Lower-trust data| M
    M --> T[Model-generated get_employee request]
    T --> V[Vulnerable tool dispatcher]
    T --> H[Hardened tool dispatcher]
    V --> DB[(SQLite: synthetic employees)]
    DB --> X[Unauthorized tool-result disclosure]
    H --> N[Denied: tool not permitted]
    V --> A[JSONL audit log]
    H --> A
```

This illustrates the **attack-comparison harness**. It does not imply the ordinary interactive agent exposes the deliberately vulnerable dispatcher.

The editable, more detailed version is in [`docs/architecture.md`](docs/architecture.md).

## Technology

- **Python** — agent, tools, test harness and auditing
- **Ollama / Llama 3.2 3B** — locally hosted language model and structured tool requests
- **SQLite** — fictional employee records
- **Streamlit / pandas** — results dashboard
- **unittest** — regression tests
- **Mermaid** — editable architecture diagram
- **JSON / JSONL** — recorded evaluations and audit events

## Repository layout

```text
agentsec-lab/
├── src/                   # Agent, LLM, SQLite, document and tool components
│   ├── agent.py
│   ├── llm.py
│   ├── tools.py
│   ├── vulnerable_tools.py
│   ├── database.py
│   ├── documents.py
│   ├── guards.py
│   └── audit.py
├── attacks/               # Injection payloads and controlled evaluation scripts
│   ├── injected_salary_policy.txt
│   ├── run_tool_attack.py
│   ├── evaluate_tool_attack.py
│   ├── run_audited_attack.py
│   └── evaluate_end_to_end.py
├── data/documents/        # Synthetic company policy
├── dashboard/app.py       # Streamlit dashboard
├── docs/architecture.md   # Architecture and trust-boundary notes
├── reports/               # Generated experimental results; review before publishing
├── tests/                 # unittest suite
├── assets/
│   ├── screenshots/       # Five documented evidence images
│   └── video/             # Two edited demonstration videos
├── requirements.txt
└── README.md
```

Some earlier experiment scripts may also appear under `attacks/`.

## Getting started (Kali WSL + VS Code)

Prerequisites: Python, a working virtual environment, Git, Ollama, and the `llama3.2:3b` model. Ollama must be installed separately; it is not a Python dependency.

```bash
cd ~/projects/agentsec-lab
python3 -m venv .venv             # skip if already created
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Start Ollama in another terminal if it is not already running:

```bash
ollama serve
```

In your project terminal, download the local model if needed:

```bash
ollama pull llama3.2:3b
```

Initialize the synthetic database:

```bash
python -c "from src.database import initialize_database; initialize_database()"
```

Run the interactive agent:

```bash
python -m src.main
```

Example commands inside the agent: `help`, `profile`, `ask What is prompt injection?`, `tool Show me my employee profile`, `document`, `exit`.

## Reproduce the controlled evaluation

**Run these only against the synthetic, local lab database.** The deliberately insecure dispatcher is intended for comparison, not deployment.

```bash
# Automated unit/regression tests
python -m unittest discover -s tests -v

# One model-driven unauthorized tool request, both dispatcher outcomes
python -m attacks.run_tool_attack

# Repeated tool-request/disclosure evaluation
python -m attacks.evaluate_tool_attack

# Audited comparison; writes reports/audit_log.jsonl
python -m attacks.run_audited_attack

# Legitimate-summary checks plus adversarial tool-request checks
python -m attacks.evaluate_end_to_end

# Dashboard (reads saved reports)
python -m streamlit run dashboard/app.py
```

Streamlit normally opens at `http://localhost:8501`. The dashboard displays measured results from `reports/tool_evaluation.json`, `reports/end_to_end_results.json`, and `reports/audit_log.jsonl`.

## Visual evidence

### Screenshots

1. [Tool request, vulnerable disclosure and hardened denial](assets/screenshots/01_tool_attack_comparison.png)
2. [Automated security evaluation dashboard](assets/screenshots/02_security_evaluation_dashboard.png)
3. [Architecture and trust boundaries](assets/screenshots/03_architecture_trust_boundaries.png)
4. [Structured audit trail](assets/screenshots/04_security_audit_trail.png)
5. [End-to-end validation metrics](assets/screenshots/05_end_to_end_security_validation.png)

### Demo videos

- [Demo 1 — Indirect prompt injection and tool-result disclosure](assets/video/01_prompt_injection_exploitation.mp4)
- [Demo 2 — Automated tests, audit evidence and defense validation](assets/video/02_security_validation_demo.mp4)

> Ensure the five images and two videos are actually copied into the paths above before publishing. GitHub will show broken links for files not committed to the repository.

## Security controls and limitations

- The hardened dispatcher uses a strict tool allowlist, rejects unexpected arguments, and returns only non-sensitive profile fields.
- The local agent uses a simulated `current_user_id`; this is **not real user authentication**.
- A marker-based output guard is included as a narrow research experiment; it is **not a general prompt-injection defense**.
- The LLM can still request an unauthorized tool. The observed protection comes from **server-side authorization**, not from the model reliably ignoring injected instructions.
- The evaluation compares the same generated request against two dispatchers. It does not prove the final language-model answer would reveal the returned data.
- Tests use small sample sizes, fixed synthetic data and a specific local model and prompt configuration. Broader payloads, model versions, statistical repetitions and manual summary-quality review would be required for general claims.

See [the detailed security assessment](docs/SECURITY_ASSESSMENT.md) for methodology, observations and recommended follow-up work.

## Responsible use

This project is designed for controlled learning and authorized security validation. Never test third-party AI agents, data sources or systems without permission; never commit secrets or private personnel data. Inspect generated reports and audit logs before publishing.
