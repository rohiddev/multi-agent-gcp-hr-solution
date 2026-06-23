# Enterprise Multi-Agent Service Assistant — Google ADK + Gemini

An enterprise-grade, healthcare-aware multi-agent assistant that helps employees and
operations teams find answers and complete common internal service requests across HR,
benefits, payroll, IT support, procurement, legal, compliance, facilities, and provider
operations.

This solution is designed for a healthcare enterprise context such as UnitedHealth Group
or Optum, with strong governance, PHI protection, audit logging, and responsible AI
controls. It is positioned as an **enterprise service and operations assistant**, not a
clinical diagnosis or patient-care system.

**Author:** Rohid Dev · github.com/rohiddev

---

## Architecture

```
Employee / Operations User
    ↓
FastAPI / Chat Interface / Internal Portal
    ↓
RouterAgent
    ↓
Specialist Agents
    ├── HRPolicyAgent
    ├── BenefitsAgent
    ├── PayrollAgent
    ├── ITSupportAgent
    ├── ProcurementAgent
    ├── PurchasingAgent
    ├── LegalAgent
    ├── ComplianceAgent
    ├── FacilitiesAgent
    └── ProviderOperationsAgent
    ↓
RAG / Knowledge Retrieval
    ↓
Enterprise Data Sources
    (Cloud Storage, SharePoint, ServiceNow, Workday, Confluence, Provider Ops docs)
    ↓
Gemini Model
    ↓
Answer with citations + optional workflow action
    ↓
Approved Tools / APIs
    ↓
ServiceNow / Workday / Procurement / Legal / Facilities / ITSM
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for a detailed plain-English walkthrough,
including the "Key Design Decisions — Interview Guide" section.

---

## Quickstart

```bash
# 1. Install dependencies (Python 3.11+ required)
pip install -r requirements.txt

# 2. Configure GCP credentials
gcloud auth application-default login

# 3. Enable required APIs
# Vertex AI API, Cloud Logging API, Cloud Trace API

# 4. Configure environment
cp .env.example .env
# Edit .env with GCP_PROJECT_ID, GCP_LOCATION, and retrieval backend

# 5. Run the FastAPI server
python main.py

# 6. Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "How many PTO days do I have?"}'
```

---

## Folder Structure

```
multi_agent_gcp_hr_solution/
├── main.py                           # FastAPI entry point
├── config.py                         # Centralized config with fail-fast validation
├── pyproject.toml
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── ARCHITECTURE.md                   # Detailed architecture + interview guide
├── PITCH.md                          # Executive pitch for healthcare enterprises
├── GOVERNANCE.md                     # Healthcare AI governance and responsible AI
├── USE_CASES.md                      # Common HR/enterprise use cases and mappings
├── data/policies/                    # Sample policy documents
│   ├── hr_policy/
│   ├── benefits/
│   ├── payroll/
│   ├── procurement/
│   ├── purchasing/               # Purchasing policy and approval thresholds
│   ├── legal/
│   ├── compliance/
│   ├── facilities/
│   └── provider_operations/        # Provider ops knowledge sources
├── agents/
│   ├── __init__.py
│   ├── router_agent.py               # Classifies and routes requests
│   ├── hr_policy_agent.py
│   ├── benefits_agent.py
│   ├── payroll_agent.py
│   ├── it_support_agent.py           # IT support and access requests
│   ├── procurement_agent.py
│   ├── purchasing_agent.py           # Purchase requisitions and purchasing policy
│   ├── legal_agent.py
│   ├── compliance_agent.py
│   ├── facilities_agent.py
│   └── provider_operations_agent.py  # Provider onboarding and credentialing
├── tools/
│   ├── __init__.py
│   └── enterprise_hr_tools.py      # Knowledge search, case creation, tickets, summaries
├── retrieval/
│   ├── __init__.py
│   └── retrieval.py                 # RAG backend abstraction (stub/prod)
├── observability/
│   ├── __init__.py
│   └── telemetry.py                 # Logging + Cloud Trace
├── security/
│   ├── __init__.py
│   ├── iam.py                       # ADC, Secret Manager, guardrails
│   └── governance.py                # PHI detection, audit logging, human approval
└── tests/                            # Unit tests
```

---

## Supported Domains

| Domain | Example Questions |
|---|---|
| **HR Policy** | PTO, parental leave, remote work, HR policies |
| **Benefits** | Medical, dental, 401k, insurance, wellness |
| **Payroll** | Paychecks, deductions, W2, direct deposit |
| **IT Support** | Password reset, laptop, software install, access, MFA |
| **Procurement** | Vendor strategy, sourcing, purchase orders, invoices, reimbursements |
| **Purchasing** | Buy something, purchase requisition, approval thresholds, purchase status |
| **Legal** | Contracts, NDAs, legal review, IP |
| **Compliance** | Training, audits, certifications, ethics |
| **Facilities** | Badge access, parking, maintenance, rooms |
| **Provider Operations** | Provider onboarding, credentialing, contracts, directory updates |

---

## Retrieval Backends

Set `RETRIEVAL_BACKEND` in `.env`:

| Backend | Use Case |
|---|---|
| `stub` | Development / MVP — deterministic sample answers |
| `agent_search` | Google Agent Builder / Vertex AI Search |
| `rag_engine` | Vertex AI RAG Engine managed pipeline |
| `vertex_ai_search` | Vertex AI Search enterprise connector |
| `vector_search` | Vertex AI Vector Search with custom embeddings |

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/ask` | Submit a question and get an answer |

### Example `/ask` request

```json
{
  "query": "How many PTO days do I have?",
  "user_id": "user-001",
  "session_id": "session-001"
}
```

### Example `/ask` response

```json
{
  "answer": "Full-time employees accrue 20 PTO days per year. Unused days can carry over up to 40 days.",
  "user_id": "user-001",
  "session_id": "session-001"
}
```

---

## Gemini Enterprise Agent Platform Integration

This solution is built with Google ADK, a code-first open-source framework. The same
agent definitions can be deployed to **Gemini Enterprise Agent Platform** for:

- Enterprise governance and policy enforcement
- Centralized model access and evaluation
- Production deployment and scaling
- Monitoring and optimization across departments

In the future, the FastAPI layer can be replaced or extended with Agent Engine / Cloud Run
deployment patterns managed by the Gemini Enterprise Agent Platform.

---

## Phased Rollout

| Phase | What to build | Risk |
|---|---|---|
| 1 | Router + HR Policy + Benefits + IT Support + Purchasing + stub retrieval | Low |
| 2 | Add Payroll, Procurement, Legal, Compliance, Facilities | Low |
| 3 | Add Provider Operations Agent | Medium |
| 4 | Connect real retrieval backend and enterprise data | Medium |
| 5 | Wire real ServiceNow / Workday / provider systems and approval workflows | Medium |
| 6 | Deploy to Agent Engine / Cloud Run with Gemini Enterprise Agent Platform | Medium |
| 7 | Responsible AI evaluation and production governance | Low (adds safety) |

---

## Healthcare Governance

This solution is built with healthcare-aware governance from the ground up. See:
- [GOVERNANCE.md](./GOVERNANCE.md) for PHI detection, audit logging, human-in-the-loop,
  responsible AI evaluation, and agent-specific guardrails.
- [PITCH.md](./PITCH.md) for the executive positioning and business case.
- [USE_CASES.md](./USE_CASES.md) for common HR and enterprise use case mappings.

Key controls:
- **No clinical decision-making:** Provider Operations Agent escalates any patient/member/clinical question to a human.
- **PHI detection and redaction:** All inputs are scanned for SSN, email, phone, MRN, member ID, and DOB before processing.
- **Audit logging:** Every request, tool call, and escalation is logged with user and session IDs.
- **Human approval:** High-risk actions (payroll changes, PHI access, record deletion) require human sign-off.
- **Source citations:** All policy answers cite approved documents.
- **Prompt injection protection:** Guardrails block jailbreak attempts.

---

## Running Tests

```bash
pytest
```
