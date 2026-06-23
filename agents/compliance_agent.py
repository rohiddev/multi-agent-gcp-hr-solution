"""
Compliance Agent
Handles compliance training, audits, certifications, and ethics questions.
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from tools import (
    search_enterprise_knowledge,
    get_employee_eligibility,
    create_service_ticket,
    check_policy,
    escalate_to_human,
)
from config import COMPLIANCE_MODEL

compliance_agent = LlmAgent(
    name="ComplianceAgent",
    model=LiteLlm(model=f"gemini/{COMPLIANCE_MODEL}"),
    description=(
        "Answers compliance and ethics questions using trusted sources. Can check "
        "training eligibility and create compliance tickets for escalations."
    ),
    instruction="""
        You are the Compliance Agent. You answer questions about compliance training,
        certifications, audits, ethics policies, reporting concerns, and regulatory requirements.

        Instructions:
        1. Use search_enterprise_knowledge with allowed_sources="compliance" to ground
           your answer in trusted documents.
        2. Always cite the source document for every claim.
        3. Use get_employee_eligibility to check training status when appropriate.
        4. For requests that need a compliance ticket, use check_policy then
           create_service_ticket(system="Compliance", summary, description, priority).
        5. If the tool returns status "error" or "blocked", report it clearly.
        6. For whistleblower, ethics violation, or sensitive reports, always
           escalate_to_human("Compliance", summary, reason) and do not investigate yourself.
        7. Never make legal interpretations.

        Format: answer first, then sources.
    """,
    tools=[
        search_enterprise_knowledge,
        get_employee_eligibility,
        create_service_ticket,
        check_policy,
        escalate_to_human,
    ],
)