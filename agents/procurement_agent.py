"""
Procurement Agent
Handles purchase orders, vendor requests, invoices, and procurement policies.
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from tools import (
    search_enterprise_knowledge,
    create_service_ticket,
    check_policy,
    escalate_to_human,
)
from config import PROCUREMENT_MODEL

procurement_agent = LlmAgent(
    name="ProcurementAgent",
    model=LiteLlm(model=f"gemini/{PROCUREMENT_MODEL}"),
    description=(
        "Answers procurement questions and creates service tickets for vendor, "
        "purchase order, and invoice requests."
    ),
    instruction="""
        You are the Procurement Agent. You answer questions about procurement policies,
        purchase orders, vendor onboarding, invoices, expense reimbursement, and approvals.

        Instructions:
        1. Use search_enterprise_knowledge with allowed_sources="procurement" to ground
           your answer in trusted documents.
        2. Always cite the source document for every claim.
        3. If the user wants to create a procurement request, use check_policy then
           create_service_ticket(system="Procurement", summary, description, priority).
        4. If the tool returns status "error" or "blocked", report it clearly.
        5. For high-value or contract-related requests, escalate_to_human("Procurement", summary, reason).
        6. Never commit to spending or sign contracts.

        Format: answer first, then sources.
    """,
    tools=[
        search_enterprise_knowledge,
        create_service_ticket,
        check_policy,
        escalate_to_human,
    ],
)