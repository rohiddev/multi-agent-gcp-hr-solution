# Governance and Responsible AI — Healthcare Enterprise Agent Platform

This document describes the governance, security, and responsible AI controls built into
the Enterprise Service Agent Platform. It is designed for a healthcare enterprise context
where trust, compliance, and auditability are critical.

---

## 1. Scope and Positioning

This platform is an **enterprise service and operations assistant**. It supports:
- HR, benefits, payroll, IT support, procurement, legal intake, compliance, facilities,
  and provider operations questions.

It does **NOT** support:
- Clinical diagnosis or treatment decisions
- Patient / member care recommendations
- Direct access to clinical systems without proper authorization
- Unsupervised handling of PHI or medical records

Clinical use cases require separate, regulated workflows and must be evaluated under
healthcare compliance frameworks (e.g. HIPAA, FDA guidance, state regulations).

---

## 2. Governance Pillars

```
┌─────────────────────────────────────────────────────────────────────┐
│                    GOVERNANCE FRAMEWORK                               │
├─────────────────────────────────────────────────────────────────────┤
│  1. Identity and Access Control                                     │
│  2. PHI / PII Detection and Redaction                              │
│  3. Audit Logging and Observability                                │
│  4. Human-in-the-Loop for Sensitive Actions                          │
│  5. Source-Based Answers and Grounding                               │
│  6. Prompt Injection and Safety Guardrails                          │
│  7. Data Loss Prevention                                             │
│  8. Responsible AI Evaluation                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Identity and Access Control

### Principle
The assistant must know who is asking and what they are allowed to see.

### Implementation
- All requests are authenticated via Google Cloud IAM (Application Default Credentials
  or Workload Identity in production).
- The user's identity and role are propagated through the agent session.
- Retrieval is filtered by the user's role and business unit.
- Tools call `check_policy(action, user_role, resource)` before executing write actions.

### Example
```
user_role=employee, action=read, resource=hr_policy -> ALLOWED
user_role=employee, action=modify_payroll, resource=payroll_data -> DENIED
user_role=hr_admin, action=modify_payroll, resource=payroll_data -> APPROVAL REQUIRED
```

---

## 4. PHI / PII Detection and Redaction

### Principle
No PHI or PII should be exposed to the model, logged in plain text, or sent to external
systems unless explicitly authorized.

### Implementation
- `security.governance.detect_phi(text)` scans for SSN, phone, email, MRN, member ID, and DOB.
- `security.governance.redact_phi(text)` replaces detected values with redaction tokens.
- All tool inputs are scanned before processing.
- Redaction is logged as an audit event.

### Configuration
- `PHI_REDACTION_ENABLED=true` in `.env` enables redaction.
- In production, integrate with a Cloud DLP or enterprise data classification service.

### Example
```
Input:  "My SSN is 123-45-6789 and my member ID is 987654321."
Output: "My SSN is [SSN_REDACTED] and my member ID is [MEMBER_ID_REDACTED]."
```

---

## 5. Audit Logging and Observability

### Principle
Every significant action must be recorded for compliance, security, and debugging.

### Implementation
- `security.governance.audit_event(...)` logs:
  - User ID and session ID
  - Action type (knowledge search, ticket creation, escalation, etc.)
  - Agent and tool names
  - Status (success, error, blocked)
  - Timestamp
- Cloud Logging captures structured logs.
- Cloud Trace provides request-level distributed tracing.
- Audit logs are tamper-evident and retained according to policy.

### Audit Events
| Event | When |
|---|---|
| `knowledge_search` | Every retrieval request |
| `create_hr_case` | Every HR case created |
| `create_service_ticket` | Every service ticket created |
| `escalate_to_human` | Every human escalation |
| `phi_detected` | When PHI is found in input |
| `phi_redacted` | When PHI is redacted |
| `guardrail_blocked` | When a guardrail blocks input |
| `sensitive_query` | When a query contains sensitive keywords |
| `human_approval_required` | When a high-risk action is flagged |

---

## 6. Human-in-the-Loop for Sensitive Actions

### Principle
High-risk or sensitive actions require human approval before execution.

### Implementation
- `security.governance.requires_human_approval(action, user_role, resource)` determines
  whether approval is needed.
- High-risk actions include:
  - `delete_record`
  - `modify_payroll`
  - `approve_claim`
  - `access_phi`
  - `export_member_data`
  - `terminate_employee`
- Sensitive queries (harassment, termination, whistleblower, clinical) are escalated to
  humans via `escalate_to_human`.

### Example
```python
if requires_human_approval("access_phi", user_role, "member_data"):
    return {
        "status": "blocked",
        "reason": "Human approval required to access PHI.",
        "escalation_id": "ESC-12345"
    }
```

---

## 7. Source-Based Answers and Grounding

### Principle
Every policy answer must be grounded in an approved document and include a citation.

### Implementation
- Specialist agents use `search_enterprise_knowledge` with source filters.
- Responses must cite the source document (e.g. `hr_policy/pto_policy.md`).
- If no relevant document is found, the agent must say so rather than fabricate an answer.
- Retrieval backends (Agent Search, RAG Engine, Vector Search) are configured to use only
  approved enterprise content.

---

## 8. Prompt Injection and Safety Guardrails

### Principle
The system must resist attempts to override instructions or extract harmful information.

### Implementation
- `security.iam.apply_guardrail(text)` detects common jailbreak patterns:
  - "ignore previous instructions"
  - "override policy"
  - "disregard safety"
  - "reveal system prompt"
  - "you are now"
- In production, replace the stub with Gemini safety settings, Cloud DLP, or a dedicated
  safety classifier.
- Blocked inputs are logged and returned with a clear refusal.

---

## 9. Data Loss Prevention

### Principle
Sensitive data must not leave the agent boundary improperly.

### Implementation
- PHI is redacted before model calls and tool calls.
- Secrets are stored in Secret Manager, never in `.env` or code.
- VPC Service Controls can restrict data movement.
- Output is scanned for accidental PHI leakage.

---

## 10. Responsible AI Evaluation

### Principle
Models and agents must be evaluated for safety, accuracy, and fairness before production.

### Evaluation Dimensions
| Dimension | What to Measure |
|---|---|
| Hallucination | Does the answer match the retrieved source? |
| Grounding | Does every claim have a citation? |
| Toxicity | Is the response harmful or offensive? |
| Bias | Does the response treat users unfairly? |
| Policy violations | Does the response violate enterprise policy? |
| Prompt injection | Does the model resist jailbreak attempts? |
| PHI leakage | Does the model output redacted or unauthorized data? |

### Evaluation Process
1. Build a labeled test dataset of representative queries.
2. Run the agent against the dataset.
3. Score responses against the dimensions above.
4. Fix issues and re-evaluate.
5. Promote to production only after passing thresholds.
6. Continuously monitor production traffic for drift.

---

## 11. Agent-Specific Guardrails

### Provider Operations Agent
- Never answers clinical or patient-care questions.
- Escalates any mention of patients, members, diagnoses, or treatments to a human.
- Does not access PHI or member data without explicit authorization.

### IT Support Agent
- Never provides instructions that bypass security controls.
- Does not request or display credentials.
- Escalates security incidents and outages.

### Legal / Compliance Agents
- Never provide legal advice or make binding decisions.
- Escalate contract interpretation, disputes, and ethics reports.

### HR / Benefits / Payroll Agents
- Do not make final employment decisions.
- Escalate sensitive medical, harassment, or termination topics.
- Redact PHI before creating cases or tickets.

---

## 12. Configuration

Governance controls are configured in `.env`:

```bash
# Enable PHI redaction and audit logging
PHI_REDACTION_ENABLED=true
AUDIT_LOGGING_ENABLED=true
HUMAN_APPROVAL_REQUIRED=true
SAFETY_ENABLED=true
```

---

## 13. Production Checklist

Before deploying to production:

- [ ] Service account uses Workload Identity, not downloaded keys.
- [ ] Service account has least-privilege IAM roles.
- [ ] Secret Manager is used for all credentials.
- [ ] VPC Service Controls are enabled for sensitive data.
- [ ] Cloud Audit Logs are enabled for Vertex AI and agent APIs.
- [ ] PHI redaction is validated with a test dataset.
- [ ] Human approval workflows are tested for high-risk actions.
- [ ] Responsible AI evaluation is complete and documented.
- [ ] Incident response plan is in place for safety failures.
- [ ] Data retention and deletion policies are defined.
- [ ] Legal and compliance teams have reviewed the solution.

---

## 14. References

- Google ADK: https://google.github.io/adk-docs/
- Gemini Enterprise Agent Platform: https://cloud.google.com/gemini
- Google Cloud Healthcare API security: https://cloud.google.com/healthcare-api/docs/security
- HIPAA and Google Cloud: https://cloud.google.com/security/compliance/hipaa
- Responsible AI practices: https://ai.google/responsibilities/responsible-ai-practices/
