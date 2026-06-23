"""
Healthcare-aware governance controls for the enterprise service assistant.

For a healthcare organization like UnitedHealth Group / Optum, this agent platform is
positioned as an ENTERPRISE SERVICE and OPERATIONS assistant, NOT a clinical
diagnosis or patient-care decision system. Clinical use cases require separate,
regulated workflows and FDA/healthcare compliance review.

Governance pillars:
  1. PHI detection and redaction before any model call or tool execution.
  2. Identity-aware access control (role, department, business unit).
  3. Audit logging for every user request, tool call, and model response.
  4. Human-in-the-loop for sensitive actions and low-confidence answers.
  5. Source-grounded answers with citations for all policy responses.
  6. Prompt injection and jailbreak protection.
  7. Data loss prevention (DLP) flags.
  8. Responsible AI evaluation before production release.
"""

import logging
import re
from datetime import datetime, timezone
from typing import Any

from config import PHI_REDACTION_ENABLED, AUDIT_LOGGING_ENABLED

logger = logging.getLogger(__name__)


# --- PHI / PII patterns ---
_PHI_PATTERNS = {
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "phone": re.compile(r"\b\d{3}-\d{3}-\d{4}\b"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
    "mrn": re.compile(r"\bMRN[:\s]*\d{4,}\b", re.IGNORECASE),
    "member_id": re.compile(r"\b(member|patient|subscriber)\s*id[:\s]*\d{5,}\b", re.IGNORECASE),
    "dob": re.compile(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b"),
}


class GovernanceError(Exception):
    """Raised when a request violates governance policy."""


def detect_phi(text: str) -> dict:
    """Detect potential PHI/PII in user input.

    Returns:
        dict with "found" (bool) and "matches" (list of categories).
    """
    matches = []
    for category, pattern in _PHI_PATTERNS.items():
        if pattern.search(text):
            matches.append(category)
    return {"found": bool(matches), "matches": matches}


def redact_phi(text: str) -> str:
    """Redact detected PHI/PII from text."""
    if not PHI_REDACTION_ENABLED:
        return text
    redacted = text
    for category, pattern in _PHI_PATTERNS.items():
        redacted = pattern.sub(f"[{category.upper()}_REDACTED]", redacted)
    return redacted


def audit_event(
    user_id: str,
    session_id: str,
    action: str,
    agent: str | None = None,
    tool: str | None = None,
    status: str = "ok",
    details: dict[str, Any] | None = None,
) -> None:
    """Write an audit log entry for every significant action.

    In production, this should be sent to a secure audit store (Cloud Logging,
    BigQuery, or a dedicated audit database) with tamper-evident controls.
    """
    if not AUDIT_LOGGING_ENABLED:
        return
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "session_id": session_id,
        "action": action,
        "agent": agent,
        "tool": tool,
        "status": status,
        "details": details or {},
    }
    logger.info("AUDIT %s", entry)


def classify_sensitivity(query: str) -> dict:
    """Classify whether a request is sensitive and should require human approval.

    Returns:
        dict with "sensitive" (bool), "category" (str), and "reason" (str).
    """
    lowered = query.lower()
    sensitive_keywords = {
        "harassment": "employee relations",
        "discrimination": "employee relations",
        "termination": "employment action",
        "fire": "employment action",
        "grievance": "employee relations",
        "whistleblower": "compliance/ethics",
        "patient": "clinical/patient care",
        "diagnosis": "clinical/patient care",
        "treatment": "clinical/patient care",
        "medication": "clinical/patient care",
        " phi ": "protected health information",
        "medical record": "protected health information",
        "suicide": "mental health crisis",
        "self-harm": "mental health crisis",
    }
    for keyword, category in sensitive_keywords.items():
        if keyword in lowered:
            return {"sensitive": True, "category": category, "reason": f"Detected sensitive keyword: {keyword}"}
    return {"sensitive": False, "category": "general", "reason": "No sensitive keywords detected"}


def requires_human_approval(action: str, user_role: str, resource: str) -> bool:
    """Determine whether an action requires human approval before execution.

    High-risk actions in a healthcare enterprise context should always be approved.
    """
    high_risk_actions = {
        "delete_record",
        "modify_payroll",
        "approve_claim",
        "access_phi",
        "export_member_data",
        "terminate_employee",
    }
    high_risk_resources = {"phi", "member_data", "patient_data", "payroll_data", "clinical_system"}
    if action in high_risk_actions or resource.lower() in high_risk_resources:
        return True
    if action in ("approve_request", "create_vendor_contract") and user_role not in ("manager", "admin"):
        return True
    return False
