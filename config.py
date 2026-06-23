import os
from dotenv import load_dotenv

load_dotenv()

VALID_RETRIEVAL_BACKENDS = {
    "agent_search",
    "rag_engine",
    "vertex_ai_search",
    "vector_search",
    "stub",
}

VALID_MODELS = {
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
}


def _require(key: str) -> str:
    """Return a required environment variable or raise with a clear message."""
    val = os.getenv(key)
    if not val:
        raise EnvironmentError(
            f"Required environment variable '{key}' is not set. "
            "Copy .env.example to .env and fill in your values."
        )
    return val


def _optional(key: str, default: str) -> str:
    """Return an optional environment variable, falling back to default."""
    return os.getenv(key, default)


def _boolean(key: str, default: bool) -> bool:
    """Return a boolean from a truthy/falsy env value."""
    val = os.getenv(key)
    if val is None:
        return default
    return val.lower() in ("1", "true", "yes", "on")


# --- GCP / Project ---
GCP_PROJECT_ID = _optional("GCP_PROJECT_ID", "")
GCP_LOCATION   = _optional("GCP_LOCATION", "us-central1")

# --- Model selection ---
ROUTER_MODEL      = _optional("ROUTER_MODEL",      "gemini-2.5-flash")
HR_POLICY_MODEL   = _optional("HR_POLICY_MODEL",   "gemini-2.5-flash")
BENEFITS_MODEL    = _optional("BENEFITS_MODEL",    "gemini-2.5-flash")
PAYROLL_MODEL     = _optional("PAYROLL_MODEL",     "gemini-2.5-flash")
PROCUREMENT_MODEL = _optional("PROCUREMENT_MODEL", "gemini-2.5-flash")
LEGAL_MODEL       = _optional("LEGAL_MODEL",       "gemini-2.5-pro")
COMPLIANCE_MODEL  = _optional("COMPLIANCE_MODEL",  "gemini-2.5-pro")
FACILITIES_MODEL  = _optional("FACILITIES_MODEL",  "gemini-2.5-flash")

for _name, _model in [
    ("ROUTER_MODEL", ROUTER_MODEL),
    ("HR_POLICY_MODEL", HR_POLICY_MODEL),
    ("BENEFITS_MODEL", BENEFITS_MODEL),
    ("PAYROLL_MODEL", PAYROLL_MODEL),
    ("PROCUREMENT_MODEL", PROCUREMENT_MODEL),
    ("LEGAL_MODEL", LEGAL_MODEL),
    ("COMPLIANCE_MODEL", COMPLIANCE_MODEL),
    ("FACILITIES_MODEL", FACILITIES_MODEL),
]:
    if _model not in VALID_MODELS:
        raise EnvironmentError(
            f"{_name}='{_model}' is not a supported model. "
            f"Valid values: {sorted(VALID_MODELS)}"
        )

# --- Retrieval ---
RETRIEVAL_BACKEND = _optional("RETRIEVAL_BACKEND", "stub")
if RETRIEVAL_BACKEND not in VALID_RETRIEVAL_BACKENDS:
    raise EnvironmentError(
        f"RETRIEVAL_BACKEND='{RETRIEVAL_BACKEND}' is not supported. "
        f"Valid values: {sorted(VALID_RETRIEVAL_BACKENDS)}"
    )

AGENT_SEARCH_APP  = _optional("AGENT_SEARCH_APP", "")
RAG_ENGINE_CORPUS = _optional("RAG_ENGINE_CORPUS", "")
VERTEX_AI_INDEX   = _optional("VERTEX_AI_INDEX", "")
VECTOR_INDEX_ENDPOINT = _optional("VECTOR_INDEX_ENDPOINT", "")
EMBEDDING_MODEL   = _optional("EMBEDDING_MODEL", "text-embedding-005")

# --- Guardrails ---
SAFETY_ENABLED = _boolean("SAFETY_ENABLED", True)

# --- App ---
APP_NAME  = _optional("APP_NAME", "enterprise-hr-assistant")
LOG_LEVEL = _optional("LOG_LEVEL", "INFO")
API_HOST  = _optional("API_HOST", "0.0.0.0")
API_PORT  = int(_optional("API_PORT", "8000"))

# --- Enterprise tool stubs ---
TICKETING_SYSTEM = _optional("TICKETING_SYSTEM", "")  # e.g. "servicenow", "jira"
