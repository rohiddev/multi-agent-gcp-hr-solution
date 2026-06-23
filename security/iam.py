"""
GCP security helpers for the enterprise HR assistant.

Production checklist:
  1. Use Workload Identity / IAM service account — no downloaded keys.
  2. Apply least-privilege: only Vertex AI, Agent Engine, RAG Engine, and Cloud Storage permissions.
  3. Store secrets in Secret Manager — never in .env or code.
  4. Use VPC Service Controls for sensitive data.
  5. Enable Cloud Audit Logs for every model invocation and tool call.

Minimum service account roles:
  - roles/aiplatform.user          (Vertex AI / Gemini)
  - roles/aiplatform.ragUser       (RAG Engine / Vector Search)
  - roles/retriever.agentUser      (Agent Builder / Agent Search)
  - roles/secretmanager.secretAccessor (for enterprise secrets)
  - roles/logging.logWriter
  - roles/monitoring.metricWriter
"""

import logging
from google.auth import default as google_auth_default
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import secretmanager
from google.cloud import aiplatform
from config import APP_NAME, GCP_LOCATION, GCP_PROJECT_ID

logger = logging.getLogger(__name__)


def get_credentials() -> dict:
    """Validate GCP credentials and return the current project identity.

    Used at startup to fail fast if Application Default Credentials are missing.

    Returns:
        dict with project_id, location, and service_account.

    Raises:
        EnvironmentError: If no valid credentials are found.
    """
    try:
        credentials, project_id = google_auth_default()
        if not credentials:
            raise DefaultCredentialsError("No credentials returned")
        if not project_id:
            project_id = GCP_PROJECT_ID
        if not project_id:
            raise EnvironmentError(
                "GCP_PROJECT_ID is not set and could not be inferred from ADC."
            )
        logger.info("GCP credentials OK project=%s location=%s", project_id, GCP_LOCATION)
        return {
            "project_id": project_id,
            "location": GCP_LOCATION,
            "service_account": getattr(credentials, "service_account_email", "unknown"),
        }
    except DefaultCredentialsError as e:
        raise EnvironmentError(
            "GCP Application Default Credentials (ADC) not found. "
            "Run 'gcloud auth application-default login' locally, or "
            "attach a service account in production."
        ) from e


def initialise_vertex() -> None:
    """Initialise Vertex AI SDK once at startup."""
    if not GCP_PROJECT_ID or not GCP_LOCATION:
        raise EnvironmentError("GCP_PROJECT_ID and GCP_LOCATION are required for Vertex AI.")
    aiplatform.init(project=GCP_PROJECT_ID, location=GCP_LOCATION)
    logger.info("Vertex AI initialised project=%s location=%s", GCP_PROJECT_ID, GCP_LOCATION)


def get_secret(secret_name: str) -> str:
    """Retrieve a secret string from Google Cloud Secret Manager.

    Args:
        secret_name: short name of the secret (e.g. "servicenow-api-key").

    Returns:
        The secret string value.

    Raises:
        RuntimeError: If the secret cannot be retrieved.
    """
    if not GCP_PROJECT_ID:
        raise RuntimeError("GCP_PROJECT_ID is required to use Secret Manager.")
    full_name = f"projects/{GCP_PROJECT_ID}/secrets/{secret_name}/versions/latest"
    try:
        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(request={"name": full_name})
        logger.info("Retrieved secret name=%s", secret_name)
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve secret '{secret_name}': {e}") from e


def apply_guardrail(text: str) -> dict:
    """Stub for a production guardrail policy check.

    In production, wire this to a safety classifier or Gemini safety settings.
    For now it detects obvious injection keywords and returns a structured result.

    Args:
        text: user input to check.

    Returns:
        dict with action: "NONE" or "BLOCKED" and reason.
    """
    blocked_patterns = [
        "ignore previous instructions",
        "override policy",
        "disregard safety",
        "reveal system prompt",
        "you are now",
    ]
    lowered = text.lower()
    for pattern in blocked_patterns:
        if pattern in lowered:
            logger.warning("Guardrail blocked text containing pattern=%s", pattern)
            return {"action": "BLOCKED", "reason": f"Input contains forbidden pattern: {pattern}"}
    return {"action": "NONE"}
