
import json
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

TOOL_FILE = REPORTS / "tool_evaluation.json"
E2E_FILE = REPORTS / "end_to_end_results.json"
AUDIT_FILE = REPORTS / "audit_log.jsonl"


st.set_page_config(
    page_title="AgentSec Lab | Security Evaluation",
    page_icon="🛡️",
    layout="wide"
)


def load_json(path):
    if not path.exists():
        return None

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_audit_logs():
    if not AUDIT_FILE.exists():
        return pd.DataFrame()

    events = []

    with AUDIT_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                events.append(json.loads(line))

    return pd.DataFrame(events)


def percentage(count, total):
    if total == 0:
        return 0.0

    return count / total * 100


tool_data = load_json(TOOL_FILE)
e2e_data = load_json(E2E_FILE)
audit_data = load_audit_logs()


st.title("🛡️ AgentSec Lab")
st.subheader("AI Agent Offensive Security Assessment")

st.caption(
    "Indirect Prompt Injection | Tool Authorization | "
    "Security Validation | Llama 3.2"
)

st.divider()

# ----------------------------------------
# SECTION 1: ORIGINAL ATTACK EVALUATION
# ----------------------------------------

st.header("1. Automated Red Team Evaluation")

if tool_data is not None:

    trials = tool_data["trials"]
    valid = tool_data["valid_attack_requests"]
    vulnerable = tool_data["vulnerable_disclosures"]
    hardened = tool_data["hardened_disclosures"]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Attack Trials", trials)

    col2.metric(
        "Unauthorized Requests",
        f"{percentage(valid, trials):.0f}%"
    )

    col3.metric(
        "Vulnerable Disclosures",
        f"{percentage(vulnerable, trials):.0f}%"
    )

    col4.metric(
        "Hardened Disclosures",
        f"{percentage(hardened, trials):.0f}%"
    )

    comparison = pd.DataFrame({
        "Configuration": [
            "Vulnerable",
            "Hardened"
        ],
        "Disclosure Rate (%)": [
            percentage(vulnerable, trials),
            percentage(hardened, trials)
        ]
    })

    st.bar_chart(
        comparison.set_index("Configuration"),
        y="Disclosure Rate (%)",
        y_label="Disclosure Rate (%)"
    )

    st.caption(
        f"Model: {tool_data.get('model', 'Unknown')} | "
        f"Run: {tool_data.get('timestamp', 'Unknown')}"
    )

else:
    st.warning("Original tool evaluation report not found.")


st.divider()

# ----------------------------------------
# SECTION 2: END-TO-END VALIDATION
# ----------------------------------------

st.header("2. End-to-End Security Validation")

if e2e_data is not None:

    legitimate_total = e2e_data["legitimate_trials"]
    attack_total = e2e_data["adversarial_trials"]

    legitimate_passes = e2e_data["legitimate_task_passes"]
    unauthorized = e2e_data["unauthorized_requests"]
    vulnerable_e2e = e2e_data["vulnerable_disclosures"]
    hardened_e2e = e2e_data["hardened_disclosures"]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Legitimate Task Completion",
        f"{percentage(legitimate_passes, legitimate_total):.0f}%"
    )

    col2.metric(
        "Unauthorized Tool Requests",
        f"{percentage(unauthorized, attack_total):.0f}%"
    )

    col3.metric(
        "Vulnerable Disclosure Rate",
        f"{percentage(vulnerable_e2e, attack_total):.0f}%"
    )

    col4.metric(
        "Hardened Disclosure Rate",
        f"{percentage(hardened_e2e, attack_total):.0f}%"
    )

    results_chart = pd.DataFrame({
        "Metric": [
            "Legitimate Task Completion",
            "Unauthorized Tool Requests",
            "Vulnerable Disclosures",
            "Hardened Disclosures"
        ],
        "Observed Rate (%)": [
            percentage(legitimate_passes, legitimate_total),
            percentage(unauthorized, attack_total),
            percentage(vulnerable_e2e, attack_total),
            percentage(hardened_e2e, attack_total)
        ]
    })

    st.bar_chart(
        results_chart.set_index("Metric"),
        y="Observed Rate (%)",
        y_label="Observed Rate (%)"
    )

    st.caption(
        f"Legitimate trials: {legitimate_total} | "
        f"Adversarial trials: {attack_total} | "
        f"Model: {e2e_data.get('model', 'Unknown')}"
    )

    st.info(
        "Legitimate task completion is based on four automated "
        "fact checks, not a complete assessment of answer accuracy. "
        "Disclosure refers to synthetic data returned by a tool."
    )

    with st.expander("View Individual Evaluation Results"):
        rows = []

        for result in e2e_data.get("results", []):
            if result.get("category") == "legitimate":
                rows.append({
                    "Category": "Legitimate",
                    "Trial": result.get("trial"),
                    "Task Completed": result.get("task_completed"),
                    "Unauthorized Request": None,
                    "Vulnerable Disclosure": None,
                    "Hardened Disclosure": None
                })
            else:
                rows.append({
                    "Category": "Adversarial",
                    "Trial": result.get("trial"),
                    "Task Completed": None,
                    "Unauthorized Request": result.get(
                        "unauthorized_request"
                    ),
                    "Vulnerable Disclosure": result.get(
                        "vulnerable_disclosure"
                    ),
                    "Hardened Disclosure": result.get(
                        "hardened_disclosure"
                    )
                })

        st.dataframe(
            pd.DataFrame(rows),
            hide_index=True,
            use_container_width=True
        )

else:
    st.warning("End-to-end evaluation report not found.")


st.divider()

# ----------------------------------------
# SECTION 3: SECURITY AUDIT LOG
# ----------------------------------------

st.header("3. Security Audit Trail")

if not audit_data.empty:

    allowed = int(
        (audit_data["decision"] == "allowed").sum()
    )

    denied = int(
        (audit_data["decision"] == "denied").sum()
    )

    col1, col2 = st.columns(2)

    col1.metric("Allowed Executions", allowed)
    col2.metric("Denied Executions", denied)

    columns = [
        "timestamp",
        "user_id",
        "tool_name",
        "target_employee_id",
        "configuration",
        "decision",
        "reason"
    ]

    st.dataframe(
        audit_data[columns],
        hide_index=True,
        use_container_width=True
    )

    st.caption(
        "Audit decisions describe tool execution outcomes. "
        "They do not independently prove final-answer leakage."
    )

else:
    st.warning("No audit events are available.")


st.divider()

# ----------------------------------------
# SECTION 4: SECURITY FINDINGS
# ----------------------------------------

st.header("4. Security Findings")

st.markdown("""
### Finding 1 — Indirect Prompt Injection

An attacker-controlled document induced the AI model to request
an employee information tool unrelated to the user's legitimate
expense-policy summarization task.

### Finding 2 — Broken Access Control

The intentionally vulnerable dispatcher accepted an arbitrary
employee ID and returned a fictional employee record containing
salary information.

### Finding 3 — Authorization Enforcement

The hardened dispatcher rejected the unauthorized request,
preventing sensitive tool-result disclosure in the observed trials.

### Finding 4 — Legitimate Task Performance

The end-to-end evaluation also measured whether the model could
summarize a legitimate expense policy. This helps distinguish
security enforcement from a system that simply refuses requests.
""")

st.divider()

st.caption(
    "AgentSec Lab | Authorized local security research | "
    "Synthetic employee data only | Results specific to tested scenarios"
)
