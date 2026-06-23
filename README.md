# Enterprise Multi-Agent HR Assistant — Google ADK + Gemini

An enterprise-grade multi-agent assistant that helps employees find answers and complete
common internal service requests across HR, benefits, payroll, procurement, legal,
compliance, and facilities.

**Author:** Rohid Dev · github.com/rohiddev

---

## Architecture

```
Employee
    ↓
FastAPI / Chat Interface
    ↓
RouterAgent
    ↓
Specialist Agents
    ├── HRPolicyAgent
    ├── BenefitsAgent
    ├── PayrollAgent
    ├── ProcurementAgent
    ├── LegalAgent
    ├── ComplianceAgent
    └── FacilitiesAgent
    ↓
RAG / Knowledge Retrieval
    ↓
Enterprise Data Sources
    (Cloud Storage, SharePoint, ServiceNow, Workday, Confluence)
    ↓
Gemini Model
    ↓
Answer with citations + optional workflow action
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
├── data/policies/                    # Sample policy documents
│   ├── hr_policy/
│   ├── benefits/
│   ├── payroll/
│   ├── procurement/
│   ├── legal/
│   ├── compliance/
│   └── facilities/
├── agents/
│   ├── __init__.py
│   ├── router_agent.py               # Classifies and routes requests
│   ├── hr_policy_agent.py
│   ├── benefits_agent.py
│   ├── payroll_agent.py
│   ├── procurement_agent.py
│   ├── legal_agent.py
│   ├── compliance_agent.py
│   └── facilities_agent.py
├── tools/
│   ├── __init__.py
│   └── enterprise_hr_tools.py      # Knowledge search, case creation, tickets
├── retrieval/
│   ├── __init__.py
│   └── retrieval.py                 # RAG backend abstraction (stub/prod)
├── observability/
│   ├── __init__.py
│   └── telemetry.py                 # Logging + Cloud Trace
├── security/
│   ├── __init__.py
│   └── iam.py                       # ADC, Secret Manager, guardrails
└── tests/                            # Unit tests
```

---

## Supported Domains

| Domain | Example Questions |
|---|---|
| **HR Policy** | PTO, parental leave, remote work, HR policies |
| **Benefits** | Medical, dental, 401k, insurance, wellness |
| **Payroll** | Paychecks, deductions, W2, direct deposit |
| **Procurement** | Purchase orders, vendors, invoices, reimbursements |
| **Legal** | Contracts, NDAs, legal review, IP |
| **Compliance** | Training, audits, certifications, ethics |
| **Facilities** | Badge access, parking, maintenance, rooms |

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
| 1 | Router + HR Policy + Benefits + stub retrieval | Low |
| 2 | Add Payroll, Procurement, Legal, Compliance, Facilities | Low |
| 3 | Connect real retrieval backend and enterprise data | Medium |
| 4 | Wire real ServiceNow / Workday APIs and approval workflows | Medium |
| 5 | Deploy to Agent Engine / Cloud Run with Gemini Enterprise Agent Platform | Medium |

---

## Running Tests

```bash
pytest
```
