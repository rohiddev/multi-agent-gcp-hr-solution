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
from security import apply_guardrail

logger = logging.getLogger(__name__)


def search_enterprise_knowledge(query: str, allowed_sources: str = "", tool_context: ToolContext | None = None) -> dict:
    """Search enterprise HR knowledge base and return grounded results.

    Args:
        query: Natural language question or search phrase.
        allowed_sources: Comma-separated source filter (e.g. "hr_policy,benefits").
        tool_context: Optional ADK tool context to store state.

    Returns:
        dict with status, results, and count.
    """
    try:
        guard = apply_guardrail(query)
        if guard["action"] == "BLOCKED":
            return {"status": "blocked", "reason": guard["reason"], "results": [], "result_count": 0}

        sources = [s.strip() for s in allowed_sources.split(",") if s.strip()]
        results = retrieve(query, top_k=5, allowed_sources=sources or None)

        if tool_context is not None:
            tool_context.state["last_retrieval_query"] = query
            tool_context.state["last_retrieval_results"] = results

        return {"status": "success", "results": results, "result_count": len(results)}
    except Exception as e:
        logger.exception("search_enterprise_knowledge failed query=%s", query)
        return {"status": "error", "message": str(e), "results": [], "result_count": 0}


def create_hr_case(category: str, summary: str, description: str = "") -> dict:
    """Create a new HR case in the enterprise case management system.

    Args:
        category: HR case category (e.g. "Leave", "Payroll", "Benefits").
        summary: One-line summary of the case.
        description: Detailed description.

    Returns:
        dict with status and case_id.
    """
    try:
        guard = apply_guardrail(summary)
        if guard["action"] == "BLOCKED":
            return {"status": "blocked", "reason": guard["reason"]}
        logger.info("create_hr_case category=%s summary=%s", category, summary)
        # TODO: call Workday / ServiceNow / BambooHR case API
        return {"status": "success", "case_id": f"HR-{hash(summary) % 100000:05d}", "category": category}
    except Exception as e:
        logger.exception("create_hr_case failed category=%s", category)
        return {"status": "error", "message": str(e)}


def create_service_ticket(system: str, summary: str, description: str = "", priority: str = "P3") -> dict:
    """Create a general service ticket in the enterprise ticketing system.

    Args:
        system: Ticketing system or team (e.g. "IT", "Facilities", "Legal").
        summary: One-line summary.
        description: Detailed description.
        priority: P1 | P2 | P3 | P4 (default P3).

    Returns:
        dict with status and ticket_id.
    """
    try:
        guard = apply_guardrail(summary)
        if guard["action"] == "BLOCKED":
            return {"status": "blocked", "reason": guard["reason"]}
        logger.info("create_service_ticket system=%s priority=%s summary=%s", system, priority, summary)
        # TODO: call ServiceNow / Jira / internal API
        return {"status": "success", "ticket_id": f"{system.upper()}-{hash(summary) % 100000:05d}", "priority": priority}
    except Exception as e:
        logger.exception("create_service_ticket failed system=%s", system)
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


def escalate_to_human(domain: str, summary: str, reason: str = "complex or sensitive request") -> dict:
    """Escalate a request to a human specialist.

    Args:
        domain: Domain team (e.g. "HR", "Legal", "Compliance", "Payroll").
        summary: One-line summary of the request.
        reason: Why escalation is needed.

    Returns:
        dict with status and escalation_id.
    """
    try:
        logger.info("escalate_to_human domain=%s reason=%s", domain, reason)
        return {
            "status": "success",
            "escalation_id": f"ESC-{domain.upper()}-{hash(summary) % 100000:05d}",
            "message": f"Escalated to {domain} team. A specialist will respond within 24 hours.",
        }
    except Exception as e:
        logger.exception("escalate_to_human failed domain=%s", domain)
        return {"status": "error", "message": str(e)}
