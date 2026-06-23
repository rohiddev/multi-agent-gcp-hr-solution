"""
Enterprise HR tool definitions.

Each function is a plain Python function — ADK converts them into callable tools.
All tools follow the status convention: success | error | blocked.

In production, replace stubs with real API calls to ServiceNow, Workday, Jira,
BambooHR, or your internal ticketing system. Secrets should be fetched via
security.get_secret().
"""

import logging
from google.adk.tools.tool_context import ToolContext
from retrieval import retrieve
from security import apply_guardrail, detect_phi, redact_phi, audit_event, classify_sensitivity

logger = logging.getLogger(__name__)


def search_enterprise_knowledge(
    query: str,
    allowed_sources: str = "",
    user_id: str = "unknown",
    session_id: str = "unknown",
    tool_context: ToolContext | None = None,
) -> dict:
    """Search enterprise knowledge base and return grounded, redacted results.

    Args:
        query: Natural language question or search phrase.
        allowed_sources: Comma-separated source filter (e.g. "hr_policy,benefits").
        user_id: Identity of the requester for audit logging.
        session_id: Session ID for audit logging.
        tool_context: Optional ADK tool context to store state.

    Returns:
        dict with status, results, and count.
    """
    try:
        phi = detect_phi(query)
        if phi["found"]:
            query = redact_phi(query)
            audit_event(user_id, session_id, "phi_detected", tool="search_enterprise_knowledge", details=phi)

        guard = apply_guardrail(query)
        if guard["action"] == "BLOCKED":
            audit_event(user_id, session_id, "guardrail_blocked", tool="search_enterprise_knowledge", details=guard)
            return {"status": "blocked", "reason": guard["reason"], "results": [], "result_count": 0}

        sensitivity = classify_sensitivity(query)
        if sensitivity["sensitive"]:
            audit_event(user_id, session_id, "sensitive_query", tool="search_enterprise_knowledge", details=sensitivity)

        sources = [s.strip() for s in allowed_sources.split(",") if s.strip()]
        results = retrieve(query, top_k=5, allowed_sources=sources or None)

        if tool_context is not None:
            tool_context.state["last_retrieval_query"] = query
            tool_context.state["last_retrieval_results"] = results

        audit_event(user_id, session_id, "knowledge_search", tool="search_enterprise_knowledge", status="success")
        return {"status": "success", "results": results, "result_count": len(results)}
    except Exception as e:
        logger.exception("search_enterprise_knowledge failed query=%s", query)
        audit_event(user_id, session_id, "knowledge_search", tool="search_enterprise_knowledge", status="error", details={"error": str(e)})
        return {"status": "error", "message": str(e), "results": [], "result_count": 0}


def create_hr_case(
    category: str,
    summary: str,
    description: str = "",
    user_id: str = "unknown",
    session_id: str = "unknown",
) -> dict:
    """Create a new HR case in the enterprise case management system.

    Args:
        category: HR case category (e.g. "Leave", "Payroll", "Benefits").
        summary: One-line summary of the case.
        description: Detailed description.
        user_id: Identity of the requester for audit logging.
        session_id: Session ID for audit logging.

    Returns:
        dict with status and case_id.
    """
    try:
        combined = f"{summary} {description}".strip()
        phi = detect_phi(combined)
        if phi["found"]:
            summary = redact_phi(summary)
            description = redact_phi(description)
            audit_event(user_id, session_id, "phi_redacted", tool="create_hr_case", details=phi)

        guard = apply_guardrail(summary)
        if guard["action"] == "BLOCKED":
            audit_event(user_id, session_id, "guardrail_blocked", tool="create_hr_case", details=guard)
            return {"status": "blocked", "reason": guard["reason"]}

        logger.info("create_hr_case category=%s summary=%s", category, summary)
        audit_event(user_id, session_id, "create_hr_case", tool="create_hr_case", status="success", details={"category": category})
        # TODO: call Workday / ServiceNow / BambooHR case API
        return {"status": "success", "case_id": f"HR-{hash(summary) % 100000:05d}", "category": category}
    except Exception as e:
        logger.exception("create_hr_case failed category=%s", category)
        audit_event(user_id, session_id, "create_hr_case", tool="create_hr_case", status="error", details={"error": str(e)})
        return {"status": "error", "message": str(e)}


def create_service_ticket(
    system: str,
    summary: str,
    description: str = "",
    priority: str = "P3",
    user_id: str = "unknown",
    session_id: str = "unknown",
) -> dict:
    """Create a general service ticket in the enterprise ticketing system.

    Args:
        system: Ticketing system or team (e.g. "IT", "Facilities", "Legal").
        summary: One-line summary.
        description: Detailed description.
        priority: P1 | P2 | P3 | P4 (default P3).
        user_id: Identity of the requester for audit logging.
        session_id: Session ID for audit logging.

    Returns:
        dict with status and ticket_id.
    """
    try:
        combined = f"{summary} {description}".strip()
        phi = detect_phi(combined)
        if phi["found"]:
            summary = redact_phi(summary)
            description = redact_phi(description)
            audit_event(user_id, session_id, "phi_redacted", tool="create_service_ticket", details=phi)

        guard = apply_guardrail(summary)
        if guard["action"] == "BLOCKED":
            audit_event(user_id, session_id, "guardrail_blocked", tool="create_service_ticket", details=guard)
            return {"status": "blocked", "reason": guard["reason"]}

        logger.info("create_service_ticket system=%s priority=%s summary=%s", system, priority, summary)
        audit_event(user_id, session_id, "create_service_ticket", tool="create_service_ticket", status="success", details={"system": system, "priority": priority})
        # TODO: call ServiceNow / Jira / internal API
        return {"status": "success", "ticket_id": f"{system.upper()}-{hash(summary) % 100000:05d}", "priority": priority}
    except Exception as e:
        logger.exception("create_service_ticket failed system=%s", system)
        audit_event(user_id, session_id, "create_service_ticket", tool="create_service_ticket", status="error", details={"error": str(e)})
        return {"status": "error", "message": str(e)}


def get_employee_eligibility(employee_id: str, program: str) -> dict:
    """Look up whether an employee is eligible for a specific program or benefit.

    Args:
        employee_id: Employee identifier.
        program: Program name (e.g. "parental_leave", "401k_match", "training").

    Returns:
        dict with status, eligible flag, and notes.
    """
    try:
        logger.info("get_employee_eligibility employee_id=%s program=%s", employee_id, program)
        # TODO: call Workday / HRIS API
        eligible = program in ("parental_leave", "401k_match", "annual_training")
        return {
            "status": "success",
            "eligible": eligible,
            "notes": f"Employee {employee_id} is {'eligible' if eligible else 'not eligible'} for {program}.",
        }
    except Exception as e:
        logger.exception("get_employee_eligibility failed employee_id=%s", employee_id)
        return {"status": "error", "message": str(e)}


def check_policy(action: str, user_role: str, resource: str) -> dict:
    """Check whether the requested action is permitted under enterprise policy.

    Args:
        action: Action requested (e.g. "create_case", "approve_request", "read").
        user_role: Role of the user (e.g. "employee", "manager", "hr_admin").
        resource: Resource being accessed (e.g. "payroll_data", "hr_policy").

    Returns:
        dict with allowed and reason.
    """
    try:
        logger.info("check_policy action=%s role=%s resource=%s", action, user_role, resource)
        # TODO: call enterprise policy engine / OPA / IAM
        allowed = action in ("read", "search", "create_hr_case", "create_service_ticket")
        if action in ("approve_request", "delete_record", "modify_payroll") and user_role not in ("manager", "hr_admin"):
            allowed = False
        return {
            "allowed": allowed,
            "reason": "permitted by enterprise policy" if allowed else "action requires elevated role",
        }
    except Exception as e:
        logger.exception("check_policy failed action=%s", action)
        return {"allowed": False, "reason": f"policy check error: {e}"}


def escalate_to_human(
    domain: str,
    summary: str,
    reason: str = "complex or sensitive request",
    user_id: str = "unknown",
    session_id: str = "unknown",
) -> dict:
    """Escalate a request to a human specialist.

    Args:
        domain: Domain team (e.g. "HR", "Legal", "Compliance", "Payroll").
        summary: One-line summary of the request.
        reason: Why escalation is needed.
        user_id: Identity of the requester for audit logging.
        session_id: Session ID for audit logging.

    Returns:
        dict with status and escalation_id.
    """
    try:
        phi = detect_phi(summary)
        if phi["found"]:
            summary = redact_phi(summary)
            audit_event(user_id, session_id, "phi_redacted", tool="escalate_to_human", details=phi)

        logger.info("escalate_to_human domain=%s reason=%s", domain, reason)
        audit_event(user_id, session_id, "escalate_to_human", tool="escalate_to_human", status="success", details={"domain": domain, "reason": reason})
        return {
            "status": "success",
            "escalation_id": f"ESC-{domain.upper()}-{hash(summary) % 100000:05d}",
            "message": f"Escalated to {domain} team. A specialist will respond within 24 hours.",
        }
    except Exception as e:
        logger.exception("escalate_to_human failed domain=%s", domain)
        audit_event(user_id, session_id, "escalate_to_human", tool="escalate_to_human", status="error", details={"error": str(e)})
        return {"status": "error", "message": str(e)}


def summarize_case(case_text: str, user_id: str = "unknown", session_id: str = "unknown") -> dict:
    """Summarize a long case or ticket thread for a human reviewer.

    Args:
        case_text: Long text to summarize.
        user_id: Identity of the requester for audit logging.
        session_id: Session ID for audit logging.

    Returns:
        dict with status and summary.
    """
    try:
        phi = detect_phi(case_text)
        if phi["found"]:
            case_text = redact_phi(case_text)
            audit_event(user_id, session_id, "phi_redacted", tool="summarize_case", details=phi)

        # In production, this would call a Gemini model with a controlled prompt.
        # For the MVP, we return a concise stub summary.
        sentences = [s.strip() for s in case_text.split(".") if s.strip()]
        summary = " ".join(sentences[:3]) + ("." if sentences else "No content provided.")
        audit_event(user_id, session_id, "summarize_case", tool="summarize_case", status="success")
        return {"status": "success", "summary": summary}
    except Exception as e:
        logger.exception("summarize_case failed")
        audit_event(user_id, session_id, "summarize_case", tool="summarize_case", status="error", details={"error": str(e)})
        return {"status": "error", "message": str(e)}
