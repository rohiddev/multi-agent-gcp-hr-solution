# Architecture — Plain English Guide (Enterprise HR Assistant)

This document explains how the system works piece by piece, using simple diagrams and
plain English. It also includes a "Key Design Decisions" section useful for interviews.

---

## The Big Picture

Imagine an employee named Alex who works at a large company. Alex needs to know how many
PTO days are left, or wants to request a new laptop, or has a question about parental leave.

Instead of opening five different portals and searching through PDFs, Alex opens one chat
window and asks the **Enterprise HR Assistant**. The assistant reads the question, figures
out which department is best placed to answer, looks up the official company documents, and
responds with a clear answer plus the source.

If the request needs a real action, like creating a ticket or opening a case, the assistant
checks whether Alex is allowed to do it, then triggers the action through the company's systems.

```
 ┌─────────────────────────────────────────────────────────────────────┐
 │                        EMPLOYEE (Alex)                              │
 │                                                                     │
 │  "How many PTO days do I have?"                                     │
 │  "How do I request a new laptop?"                                   │
 │  "What is the parental leave policy?"                               │
 └───────────────────────────────┬─────────────────────────────────────┘
                                 │
                                 ▼
 ┌─────────────────────────────────────────────────────────────────────┐
 │               FASTAPI APP  —  main.py                               │
 │                                                                     │
 │  • Receives the question                                            │
 │  • Validates credentials and starts tracing                         │
 │  • Creates a session and passes it to the Router Agent              │
 └───────────────────────────────┬─────────────────────────────────────┘
                                 │
                                 ▼
```

---

## Layer 1 — The Router Agent (The Receptionist)

```
 ┌─────────────────────────────────────────────────────────────────────┐
 │                      ROUTER AGENT                                   │
 │                     agents/router_agent.py                          │
 │                                                                     │
 │  Powered by: Gemini 2.5 Flash                                       │
 │  "I read every employee request and decide which specialist        │
 │   should handle it."                                                │
 │                                                                     │
 │  ┌─────────────────────────────────────────────────────────────┐    │
 │  │  Routing Rules (plain English)                              │    │
 │  │                                                             │    │
 │  │  PTO, vacation, sick leave, parental leave, HR policies   │    │
 │  │    -> HR Policy Agent                                       │    │
 │  │                                                             │    │
 │  │  Medical, dental, vision, 401k, insurance, wellness       │    │
 │  │    -> Benefits Agent                                        │    │
 │  │                                                             │    │
 │  │  Paycheck, salary, deductions, W2, tax, direct deposit    │    │
 │  │    -> Payroll Agent                                         │    │
 │  │                                                             │    │
 │  │  Vendor, purchase order, invoice, reimbursement           │    │
 │  │    -> Procurement Agent                                     │    │
 │  │                                                             │    │
 │  │  Contract, NDA, legal review, IP                            │    │
 │  │    -> Legal Agent                                           │    │
 │  │                                                             │    │
 │  │  Policy, audit, training, certification, ethics            │    │
 │  │    -> Compliance Agent                                      │    │
 │  │                                                             │    │
 │  │  Badge, building, parking, maintenance, room              │    │
 │  │    -> Facilities Agent                                      │    │
 │  └─────────────────────────────────────────────────────────────┘    │
 └──────┬──────────────────────────────────────────────────────────────┘
        │
        │ routes to
        ▼
 ┌─────────────────────────────────────────────────────────────────────┐
 │  Specialist Agents (HR Policy, Benefits, Payroll, Procurement,       │
 │  Legal, Compliance, Facilities)                                       │
 └─────────────────────────────────────────────────────────────────────┘
```

---

## Layer 2 — Specialist Agents (The Domain Experts)

Each specialist agent is a focused mini-assistant for one business domain.

```
 ┌─────────────────────────────────────────────────────────────────────┐
 │                    HR POLICY AGENT                                  │
 │                                                                     │
 │  "I answer questions about HR policies, PTO, leave, and conduct.   │
 │   I can create an HR case or escalate sensitive topics."          │
 │                                                                     │
 │  Tools:                                                             │
 │   • search_enterprise_knowledge (sources: hr_policy)                │
 │   • create_hr_case                                                │
 │   • check_policy                                                  │
 │   • escalate_to_human                                             │
 └─────────────────────────────────────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────────────────────┐
 │                     BENEFITS AGENT                                  │
 │                                                                     │
 │  "I answer benefits questions and can check employee eligibility."  │
 │                                                                     │
 │  Tools:                                                             │
 │   • search_enterprise_knowledge (sources: benefits)                │
 │   • get_employee_eligibility                                       │
 │   • create_hr_case                                                │
 │   • check_policy                                                  │
 │   • escalate_to_human                                             │
 └─────────────────────────────────────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────────────────────┐
 │                     PAYROLL AGENT                                   │
 │                                                                     │
 │  "I answer payroll questions and can create payroll cases."       │
 │                                                                     │
 │  Tools:                                                             │
 │   • search_enterprise_knowledge (sources: payroll)                 │
 │   • get_employee_eligibility                                       │
 │   • create_hr_case                                                │
 │   • check_policy                                                  │
 │   • escalate_to_human                                             │
 └─────────────────────────────────────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────────────────────┐
 │                    PROCUREMENT AGENT                                │
 │                                                                     │
 │  "I answer procurement questions and create procurement tickets." │
 │                                                                     │
 │  Tools:                                                             │
 │   • search_enterprise_knowledge (sources: procurement)             │
 │   • create_service_ticket (system: Procurement)                     │
 │   • check_policy                                                  │
 │   • escalate_to_human                                             │
 └─────────────────────────────────────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────────────────────┐
 │                     LEGAL AGENT                                     │
 │                                                                     │
 │  "I answer legal process questions and create legal intake tickets."│
 │   I always escalate legal judgment to a human attorney."           │
 │                                                                     │
 │  Tools:                                                             │
 │   • search_enterprise_knowledge (sources: legal)                   │
 │   • create_service_ticket (system: Legal)                         │
 │   • check_policy                                                  │
 │   • escalate_to_human                                             │
 └─────────────────────────────────────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────────────────────┐
 │                    COMPLIANCE AGENT                                 │
 │                                                                     │
 │  "I answer compliance and ethics questions and can check training  │
 │   status. Sensitive reports always escalate to a human."           │
 │                                                                     │
 │  Tools:                                                             │
 │   • search_enterprise_knowledge (sources: compliance)              │
 │   • get_employee_eligibility                                       │
 │   • create_service_ticket (system: Compliance)                    │
 │   • check_policy                                                  │
 │   • escalate_to_human                                             │
 └─────────────────────────────────────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────────────────────┐
 │                    FACILITIES AGENT                                 │
 │                                                                     │
 │  "I answer facilities questions and create building/maintenance  │
 │   tickets. Safety issues always escalate to a human."              │
 │                                                                     │
 │  Tools:                                                             │
 │   • search_enterprise_knowledge (sources: facilities)              │
 │   • create_service_ticket (system: Facilities)                    │
 │   • escalate_to_human                                             │
 └─────────────────────────────────────────────────────────────────────┘
```

---

## Layer 3 — Tools (The Connectors to Real Systems)

```
 ┌─────────────────────────────────────────────────────────────────────┐
 │              TOOLS  —  tools/enterprise_hr_tools.py                │
 │                                                                     │
 │  Tools are the hands of the agents. An agent thinks; a tool acts.  │
 │                                                                     │
 │  ┌─────────────────────────────────────────────────────────────┐   │
 │  │  search_enterprise_knowledge                                │   │
 │  │    1. Guardrail check on user input                         │   │
 │  │    2. Retrieve documents from RAG backend                   │   │
 │  │    3. Return results with content, source, and score         │   │
 │  └─────────────────────────────────────────────────────────────┘   │
 │  ┌─────────────────────────────────────────────────────────────┐   │
 │  │  create_hr_case                                             │   │
 │  │    1. Guardrail check on summary                              │   │
 │  │    2. Create case in HRIS / ServiceNow / Workday              │   │
 │  │    3. Return case_id                                         │   │
 │  └─────────────────────────────────────────────────────────────┘   │
 │  ┌─────────────────────────────────────────────────────────────┐   │
 │  │  create_service_ticket                                      │   │
 │  │    1. Guardrail check on summary                              │   │
 │  │    2. Create ticket in ServiceNow / Jira / internal system   │   │
 │  │    3. Return ticket_id and priority                         │   │
 │  └─────────────────────────────────────────────────────────────┘   │
 │  ┌─────────────────────────────────────────────────────────────┐   │
 │  │  get_employee_eligibility                                   │   │
 │  │    1. Look up employee eligibility in HRIS                   │   │
 │  │    2. Return eligible flag and notes                         │   │
 │  └─────────────────────────────────────────────────────────────┘   │
 │  ┌─────────────────────────────────────────────────────────────┐   │
 │  │  check_policy                                               │   │
 │  │    1. Check role and action against enterprise policy        │   │
 │  │    2. Return allowed flag and reason                         │   │
 │  └─────────────────────────────────────────────────────────────┘   │
 │  ┌─────────────────────────────────────────────────────────────┐   │
 │  │  escalate_to_human                                          │   │
 │  │    1. Hand off to the right human team                       │   │
 │  │    2. Return escalation_id and SLA message                   │   │
 │  └─────────────────────────────────────────────────────────────┘   │
 │                                                                     │
 │  All tools return:                                                  │
 │    {"status": "success"}  -> worked                                  │
 │    {"status": "error"}    -> failed with message                     │
 │    {"status": "blocked"}  -> guardrail or policy blocked             │
 └─────────────────────────────────────────────────────────────────────┘
```

---

## Layer 4 — RAG / Knowledge Retrieval

```
 ┌─────────────────────────────────────────────────────────────────────┐
 │         RETRIEVAL LAYER  —  retrieval/retrieval.py                  │
 │                                                                     │
 │  "I find the right documents for the question. The agent does     │
 │   not know which backend I use."                                     │
 │                                                                     │
 │  Backends (choose one in .env):                                     │
 │  ┌───────────────┐  ┌───────────────┐  ┌─────────────────────┐    │
 │  │ stub          │  │ agent_search  │  │ rag_engine          │    │
 │  │ (development) │  │ (managed)     │  │ (managed RAG)       │    │
 │  └───────────────┘  └───────────────┘  └─────────────────────┘    │
 │  ┌─────────────────────┐  ┌─────────────────────┐                 │
 │  │ vertex_ai_search    │  │ vector_search       │                 │
 │  │ (enterprise search) │  │ (custom embeddings) │                 │
 │  └─────────────────────┘  └─────────────────────┘                 │
 │                                                                     │
 │  Retrieval flow:                                                    │
 │    1. User question comes in                                        │
 │    2. Backend searches approved documents                           │
 │    3. Top-k passages returned with source and score                 │
 │    4. Agent uses only those passages to build the answer             │
 │    5. Every claim cites its source document                          │
 └─────────────────────────────────────────────────────────────────────┘
```

---

## Layer 5 — Supporting Infrastructure

```
 ┌─────────────────────────────────────────────────────────────────────┐
 │              CONFIG  —  config.py                                   │
 │                                                                     │
 │  Reads all settings from .env. Validates at startup.              │
 │  If a setting is wrong, the app stops immediately with a clear      │
 │  error message.                                                      │
 │                                                                     │
 │  Key settings:                                                      │
 │    GCP_PROJECT_ID    <- Google Cloud project                        │
 │    GCP_LOCATION      <- Vertex AI region                            │
 │    RETRIEVAL_BACKEND <- stub | agent_search | rag_engine | ...     │
 │    *_MODEL           <- Gemini model for each agent                 │
 │    LOG_LEVEL         <- logging verbosity                           │
 └─────────────────────────────────────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────────────────────┐
 │              SECURITY  —  security/iam.py                           │
 │                                                                     │
 │  get_credentials()                                                  │
 │    Validates GCP Application Default Credentials at startup.      │
 │    Fails fast if the service account is missing.                     │
 │                                                                     │
 │  initialise_vertex()                                                │
 │    Initialises Vertex AI SDK once.                                   │
 │                                                                     │
 │  get_secret(name)                                                   │
 │    Retrieves secrets from Secret Manager. Never store in .env.      │
 │                                                                     │
 │  apply_guardrail(text)                                              │
 │    Checks input for prompt injection or harmful content.            │
 │    Returns BLOCKED or NONE.                                          │
 └─────────────────────────────────────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────────────────────┐
 │           OBSERVABILITY  —  observability/telemetry.py                │
 │                                                                     │
 │  Cloud Logging                                                      │
 │    Every action, tool call, and error is logged.                   │
 │                                                                     │
 │  Cloud Trace                                                        │
 │    A visual timeline of every request across agents.               │
 │                                                                     │
 │  Setup is called once at startup and is idempotent.                 │
 └─────────────────────────────────────────────────────────────────────┘
```

---

## Full End-to-End Flow

```
  Alex
   │
   │  "How many PTO days do I have?"
   │
   ▼
 ┌──────────────────────────────────────────────────────────────────────┐
 │  FastAPI /ask endpoint                                               │
 │  • Creates user/session IDs                                          │
 │  • Starts a trace span                                               │
 │  • Passes request to Router Agent                                    │
 └─────────────────────────────────┬────────────────────────────────────┘
                                   │
                                   ▼
 ┌──────────────────────────────────────────────────────────────────────┐
 │  ROUTER AGENT (Gemini Flash)                                         │
 │  "This is an HR policy question -> HRPolicyAgent"                   │
 └─────────────────────────────────┬────────────────────────────────────┘
                                   │
                                   ▼
 ┌──────────────────────────────────────────────────────────────────────┐
 │  HR POLICY AGENT (Gemini Flash)                                      │
 │  1. search_enterprise_knowledge("PTO days", allowed_sources="hr_policy")│
 │     -> retrieve from RAG backend                                      │
 │     -> returns: "Full-time employees accrue 20 PTO days per year..." │
 │  2. Builds answer with citation                                       │
 └─────────────────────────────────┬────────────────────────────────────┘
                                   │
                                   │
                                   ▼
 ┌──────────────────────────────────────────────────────────────────────┐
 │  Router Agent synthesizes final answer                               │
 └─────────────────────────────────┬────────────────────────────────────┘
                                   │
                                   ▼
  Alex  <--  "Full-time employees accrue 20 PTO days per year.           │
              Unused days can carry over up to 40 days.                │
              Source: hr_policy/pto_policy.md"
```

---

## What Lives Where — File Map

```
  multi_agent_gcp_hr_solution/
  │
  ├── main.py                  <- START HERE. FastAPI app and agent runner.
  ├── config.py                <- All settings. Validates at startup.
  ├── .env                     <- Private settings (never committed).
  ├── .env.example             <- Template showing every setting.
  ├── pyproject.toml           <- Python version and dependencies.
  ├── README.md                <- Quickstart, API, and deployment.
  ├── ARCHITECTURE.md          <- This document.
  │
  ├── data/policies/           <- Sample enterprise documents.
  │
  ├── agents/                  <- All agent definitions.
  │   ├── router_agent.py      <- Classifies and routes requests.
  │   ├── hr_policy_agent.py
  │   ├── benefits_agent.py
  │   ├── payroll_agent.py
  │   ├── procurement_agent.py
  │   ├── legal_agent.py
  │   ├── compliance_agent.py
  │   └── facilities_agent.py
  │
  ├── tools/                   <- The connectors to real systems.
  │   └── enterprise_hr_tools.py
  │
  ├── retrieval/               <- RAG backend abstraction.
  │   └── retrieval.py
  │
  ├── observability/           <- Logging and tracing setup.
  │   └── telemetry.py
  │
  ├── security/                <- Credential and guardrail helpers.
  │   └── iam.py
  │
  └── tests/                   <- Unit tests.
```

---

## Key Design Decisions — Interview Guide

This section explains the important architectural choices and the reasoning behind them.

---

### 1. Why use a Router Agent instead of one big agent?

**Decision:** One Router Agent delegates to seven specialist agents.

**Why:**
A single agent trying to answer HR, benefits, payroll, legal, compliance, procurement,
and facilities questions becomes unreliable. Domain-specific prompts and tools are easier
to test, tune, and secure. New domains can be added without changing the router.

**Interview angle:** "This is the microservices principle applied to agents: separation of
concerns, independent failure domains, and composability."

---

### 2. Why RAG instead of letting the model answer from its own knowledge?

**Decision:** Every specialist agent must use search_enterprise_knowledge and cite sources.

**Why:**
Company policies change. A model answering from training data could cite an outdated policy
or invent a policy that does not exist. RAG grounds answers in the latest approved documents.

**Interview angle:** "RAG gives us auditability and correctness. Every answer is traceable
to a specific document version, which is essential for compliance and employee trust."

---

### 3. Why three tool return states: success, error, blocked?

**Decision:** Tools return structured dicts, never raise exceptions.

**Why:**
If a tool crashes, the agent loop fails. Structured returns let the agent reason about the
failure and respond gracefully. The "blocked" state specifically signals a guardrail or policy
intervention, which is different from a technical error.

**Interview angle:** "Tool boundaries must be hardened. The agent should receive a signal it
can reason about, not a raw stack trace."

---

### 4. Why check_policy before creating a case or ticket?

**Decision:** Every write action goes through a policy check.

**Why:**
Without a policy gate, any employee could create a case or ticket for any action, regardless
of role. The check_policy step mirrors enterprise IAM/RBAC and creates an audit trail.

**Interview angle:** "We apply least privilege at the agent layer. No action executes without
an explicit permitted verdict, preventing privilege escalation through the AI interface."

---

### 5. Why call get_credentials and initialise_vertex at startup?

**Decision:** All credential validation and SDK initialisation happens once at module load.

**Why:**
Failing at startup is better than failing mid-request. A misconfigured service account is
caught during boot, not when an employee is waiting for an answer.

**Interview angle:** "Fail fast on infrastructure dependencies. The health check should fail
at boot, not at runtime."

---

### 6. Why setup_telemetry is idempotent and called once?

**Decision:** Observability setup is guarded by a module-level singleton.

**Why:**
Repeated initialisation would create duplicate logging handlers and TracerProviders, leading
to log flooding and memory growth in a long-running service.

**Interview angle:** "Shared resources like logging, tracing, and database pools should be
initialised once and reused."

---

### 7. Why UUID-based user_id and session_id?

**Decision:** run() generates random IDs if not provided.

**Why:**
Hardcoded session IDs cause context bleed between users. UUIDs provide the minimum session
isolation required for a multi-user system.

**Interview angle:** "Session isolation is a correctness requirement. Hardcoded IDs are a bug,
not a design shortcut."

---

### 8. Why always escalate sensitive topics to a human?

**Decision:** Legal, medical, harassment, termination, safety, and whistleblower topics must
escalate to a human.

**Why:**
LLMs are not reliable for high-stakes personal or legal decisions. A human-in-the-loop is
required for accountability, empathy, and legal protection.

**Interview angle:** "AI is a triage and self-service layer, not a replacement for human
judgment in sensitive matters."

---

### 9. Why use LiteLLM with the `gemini/` prefix?

**Decision:** Agents use `LiteLlm(model="gemini/{MODEL_NAME}")` to connect ADK to Vertex AI.

**Why:**
ADK natively supports the Gemini API. LiteLLM provides a unified model interface, making it
easy to switch between Gemini models or even experiment with other providers without
rewriting agent code.

**Interview angle:** "LiteLLM decouples the agent framework from the model provider. This
makes model upgrades and cost optimisation straightforward."

---

### 10. Why a configurable retrieval backend?

**Decision:** The RAG backend is selected by a single environment variable.

**Why:**
Different enterprises have different data sources and maturity levels. The stub backend
lets developers run locally without any cloud setup. Production backends can be swapped in
without changing agent code.

**Interview angle:** "We used the strategy pattern. The agents depend on the `retrieve()`
interface, not a specific backend implementation, so the system adapts to different
enterprise environments."

---

## Glossary — Plain English Definitions

| Term | What it actually means |
|---|---|
| **Agent** | A piece of AI that can reason, make decisions, and call tools |
| **Router Agent** | The agent that reads the request and picks the right specialist |
| **RAG** | Retrieval-Augmented Generation — look up documents before answering |
| **Tool** | A Python function the agent can call to interact with a real system |
| **ADK** | Google Agent Development Kit — the open-source code-first framework |
| **Gemini** | Google's family of AI models used for reasoning |
| **Vertex AI** | Google Cloud's managed AI platform |
| **Gemini Enterprise Agent Platform** | Google's platform to deploy, govern, and scale agents |
| **ADC** | Application Default Credentials — automatic GCP authentication |
| **Cloud Trace** | GCP tool showing a timeline of every request |
| **Cloud Logging** | GCP tool storing all log messages |
| **Secret Manager** | GCP service for storing passwords and API keys |
| **Vector Search** | A search technique that finds similar documents using numerical embeddings |
| **Policy Engine** | A system that decides whether an action is allowed |
| **Escalation** | Handing a request to a human specialist |
| **Prompt Injection** | An attack where a user tries to override the agent's instructions |
| **Guardrail** | A safety check that blocks harmful or disallowed inputs |
