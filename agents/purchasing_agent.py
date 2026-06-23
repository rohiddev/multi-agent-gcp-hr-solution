"""
Purchasing Agent
Handles purchase requisitions, purchasing policy questions, and purchase order status.

This agent is dedicated to the purchasing workflow, which is often distinct from
procurement strategy (vendor selection, contracts, sourcing). It helps employees:
- Create a purchase requisition
- Check the status of an existing requisition
- Understand approval thresholds and purchasing policies
- Route high-value or non-standard purchases to the right approvers
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from tools import (
    search_enterprise_knowledge,
    create_purchase_requisition,
    get_purchase_requisition_status,
    check_policy,
    escalate_to_human,
)
from config import PURCHASING_MODEL

purchasing_agent = LlmAgent(
    name="PurchasingAgent",
    model=LiteLlm(model=f"gemini/{PURCHASING_MODEL}"),
    description=(
        "Answers purchasing policy questions and helps employees create purchase "
        "requisitions and check their status."
    ),
    instruction="""
        You are the Purchasing Agent. You handle employee purchasing requests and
        policy questions.

        Your responsibilities:
        1. Use search_enterprise_knowledge with allowed_sources="purchasing" to answer
           questions about purchasing thresholds, approval workflows, and policies.
        2. Always cite the source document for every claim.
        3. When the user wants to buy something, use create_purchase_requisition.
        4. When the user asks about a requisition, use get_purchase_requisition_status.
        5. Use check_policy before approving or escalating any non-standard request.
        6. For high-value, urgent, or complex purchases, escalate_to_human("Purchasing", summary, reason).
        7. If the tool returns status "error" or "blocked", report it clearly.
        8. Never commit the organization to spending or bypass approval workflows.

        Approval thresholds:
        - Under $1,000: manager approval
        - $1,000 to $4,999: manager + department head approval
        - $5,000 and above: manager + department head + finance approval

        Format: answer first, then sources or next steps.
    """,
    tools=[
        search_enterprise_knowledge,
        create_purchase_requisition,
        get_purchase_requisition_status,
        check_policy,
        escalate_to_human,
    ],
)
