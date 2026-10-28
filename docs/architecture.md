
# AgentSec Lab — Security Architecture

## AI Agent Prompt Injection and Authorization Assessment

```mermaid
flowchart TB
    U["Legitimate User<br/>Expense Policy Summary"]
    D["Untrusted Expense Policy<br/>Attacker-Controlled Instructions"]
    L["Local AI Model<br/>Llama 3.2 3B"]
    R["Model-Generated Tool Request<br/>get_employee(employee_id=2)"]

    V["Vulnerable Dispatcher<br/>No Employee Authorization"]
    H["Hardened Dispatcher<br/>Tool Allowlist and Validation"]

    DB[("SQLite Database<br/>Synthetic Employee Records")]
    EX["Unauthorized Record Returned<br/>Salary Included"]
    BL["Access Denied<br/>Tool Not Permitted"]
    A["Structured Security Audit Log"]

    U --> L
    D -->|"Untrusted document content"| L
    L --> R

    R -->|"Identical test request"| V
    R -->|"Identical test request"| H

    V --> DB
    DB --> EX
    H --> BL

    V --> A
    H --> A

    classDef user fill:#1e3a5f,stroke:#60a5fa,color:#ffffff
    classDef untrusted fill:#78350f,stroke:#f59e0b,color:#ffffff
    classDef model fill:#334155,stroke:#94a3b8,color:#ffffff
    classDef vulnerable fill:#7f1d1d,stroke:#f87171,color:#ffffff
    classDef hardened fill:#14532d,stroke:#4ade80,color:#ffffff

    class U user
    class D untrusted
    class L,R model
    class V,EX vulnerable
    class H,BL hardened
```

## Trust Boundaries

1. Untrusted documents must be treated as data, not instructions.
2. LLM-generated tool requests must never constitute authorization.
3. The Python dispatcher must validate permitted operations.
4. Sensitive database fields must remain inaccessible without authorization.
5. Security audit logs record tool execution outcomes.

## Tested Security Finding

An attacker-controlled expense policy induced the local model to
request the record of another fictional employee.

The deliberately vulnerable dispatcher returned the employee record,
including salary information.

The hardened dispatcher rejected the same tool request.

## Evaluation Scope

- Local model: Llama 3.2 3B
- Database: SQLite with synthetic employee records
- Attack type: Indirect prompt injection
- Impact: Unauthorized tool-result disclosure
- Defense: Python tool allowlist and authorization boundary
- Evidence: Automated trials and structured audit logs

The diagram represents the isolated attack-comparison harness.
It does not imply that the ordinary interactive agent exposes
the deliberately vulnerable dispatcher.
```
