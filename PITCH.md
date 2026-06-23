# Executive Pitch — Optum Enterprise Service Agent Platform

## One-sentence value proposition

Build a single, governed, AI-powered front door for Optum and UHG employees and
operations teams to get answers, create tickets, and route requests across HR, IT,
procurement, legal, compliance, facilities, and provider operations.

---

## The problem

Optum and UnitedHealth Group operate at massive scale across healthcare delivery,
insurance, pharmacy, and technology. Employees and operations teams face:

- **Fragmented support channels:** HR, IT, procurement, legal, compliance, and facilities
  each have their own portals, forms, and contact points.
- **High ticket volume:** Large teams spend hours answering repeat questions.
- **Slow response times:** Simple requests wait in queues because routing is manual.
- **Inconsistent answers:** Policies change, and different teams answer the same question differently.
- **Governance risk:** Healthcare requires strict controls around PHI, auditability, and responsible AI.

The result is frustrated employees, overloaded operations teams, and unnecessary cost.

---

## The solution

**Optum Enterprise Service Agent Platform** — a multi-agent assistant built with Google ADK
and Gemini Enterprise Agent Platform.

```
Employee / Operations User
        ↓
Chat UI / Internal Portal / FastAPI API
        ↓
Router Agent
        ↓
Specialist Agents
        ↓
Trusted Enterprise Knowledge (RAG)
        ↓
Gemini Model
        ↓
Answer with citations + recommended action
        ↓
Approved Tools / APIs
        ↓
ServiceNow / Workday / Procurement / Legal / Facilities / ITSM
```

---

## Why Google ADK and Gemini Enterprise Agent Platform

| Layer | Technology | Role |
|---|---|---|
| **Agent framework** | Google ADK | Code-first build, debug, and deploy agents |
| **Enterprise platform** | Gemini Enterprise Agent Platform | Govern, scale, monitor, and optimize agents |
| **Reasoning** | Gemini | Answer generation and intent classification |
| **Retrieval** | Vertex AI Search / RAG Engine / Vector Search | Trusted enterprise knowledge |
| **Hosting** | Cloud Run / Agent Engine | Secure API and service deployment |
| **Identity** | IAM / Workload Identity | Role-based access control |
| **Observability** | Cloud Logging / Cloud Trace | Audit trails and performance monitoring |
| **Secrets** | Secret Manager | Secure credential storage |

Google ADK gives us a production-grade agent loop: sessions, tool calling, streaming,
sub-agent delegation, and a built-in web UI for testing. Gemini Enterprise Agent Platform
provides the governance layer required for a regulated healthcare enterprise: policy
enforcement, model evaluation, deployment management, and responsible AI controls.

---

## Agent design

### Router Agent
Understands the request and sends it to the right specialist.

Examples:
- PTO question → **HR Policy Agent**
- Paycheck issue → **Payroll Agent**
- Laptop request → **IT Support Agent**
- Vendor contract → **Legal Intake Agent**
- Purchase request / requisition → **Purchasing Agent**
- Procurement strategy / sourcing → **Procurement Agent**
- Badge issue → **Facilities Agent**
- Training requirement → **Compliance Agent**
- Provider credentialing → **Provider Operations Agent**

### Specialist Agents

| Agent | Domain | Sample Capabilities |
|---|---|---|
| HR Policy Agent | PTO, leave, remote work, HR policies | Answer with citations, create HR case |
| Benefits Agent | Medical, dental, 401k, insurance | Eligibility lookup, benefits case |
| Payroll Agent | Paycheck, deductions, W2, tax | Payroll case, policy check |
| IT Support Agent | Password resets, laptop, access, MFA | IT ticket creation, knowledge lookup |
| Procurement Agent | Vendor strategy, sourcing, invoices | Procurement intake ticket, policy check |
|| Purchasing Agent | Requisitions, approval thresholds, purchase status | Create requisition, status lookup |
| Legal Intake Agent | Contracts, NDAs, legal review | Legal intake ticket, human escalation |
| Compliance Agent | Training, audits, ethics | Training status, compliance ticket |
| Facilities Agent | Badge, building, parking, maintenance | Facilities ticket, safety escalation |
| Provider Operations Agent | Provider onboarding, credentialing, contracts | Provider ops ticket, human escalation |

---

## Healthcare-specific governance

This platform is explicitly positioned as an **enterprise service and operations assistant**,
not a clinical decision-making system. Clinical use cases require separate, regulated
workflows.

Built-in controls:

- **No clinical diagnosis or treatment advice.** Provider Operations Agent escalates any
  patient/member/clinical question to a human.
- **PHI detection and redaction.** All user inputs are scanned for SSN, phone, email, MRN,
  member ID, and DOB patterns before processing.
- **Identity-aware access control.** Retrieval and actions respect the user's role and
  department.
- **Audit logging.** Every request, tool call, and escalation is logged with user ID and
  session ID.
- **Human approval for high-risk actions.** Payroll changes, record deletion, provider data
  export, and access to PHI require human sign-off.
- **Source citations required.** All policy answers must cite an approved document.
- **Prompt injection protection.** Guardrails detect jailbreak attempts and disallowed topics.
- **Data loss prevention.** Sensitive content is redacted before leaving the agent loop.
- **Responsible AI evaluation.** Model responses are evaluated for hallucination, toxicity,
  and policy violations before production release.

---

## Business outcomes

| Metric | Expected Impact |
|---|---|
| Ticket deflection rate | 30–50% of repeat questions answered without human intervention |
| Average response time | From hours/days to seconds for common questions |
| Policy consistency | Single source of truth with citation-backed answers |
| HR / IT / Ops workload | Reduced first-tier support burden |
| Compliance posture | Audit trail and PHI controls built in |
| Employee experience | One front door for all internal services |
| Provider operations | Faster onboarding and credentialing status lookups |

---

## Phased rollout

| Phase | Scope | Risk |
|---|---|---|
| 1 | Router + HR Policy + Benefits + IT Support + stub retrieval | Low |
| 2 | Add Payroll, Procurement, Legal, Compliance, Facilities | Low |
| 3 | Add Provider Operations Agent | Medium |
| 4 | Connect real RAG backend and enterprise data | Medium |
| 5 | Wire ServiceNow / Workday / provider systems | Medium |
| 6 | Deploy to Cloud Run / Agent Engine with Gemini Enterprise Agent Platform | Medium |
| 7 | Responsible AI evaluation and production governance | Low (adds safety) |

---

## Why this fits Optum / UHG

- **Scale:** Handles thousands of daily employee and operations requests.
- **Governance:** Meets healthcare expectations for PHI protection, auditability, and
  human oversight.
- **Platform thinking:** A reusable agent pattern that can expand to other use cases beyond
  enterprise services.
- **Responsible AI:** Aligns with UHG/Optum public commitments to responsible AI in healthcare.
- **Cost efficiency:** Reduces manual support cost while improving service quality.

---

## Executive summary

The Optum Enterprise Service Agent Platform turns fragmented internal support into a single,
governed AI-powered experience. It uses Google ADK to build specialist agents, Gemini for
reasoning, Vertex AI for trusted retrieval, and Gemini Enterprise Agent Platform for
enterprise-scale governance and deployment. For a healthcare organization, it is designed
from the ground up with PHI protection, audit logging, human-in-the-loop controls, and
source-based answers.
