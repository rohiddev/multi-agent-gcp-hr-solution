"""
IT Support Agent
Handles common IT requests, access issues, password resets, laptop requests, and
software install requests. This agent is critical for large healthcare enterprises
where employees need reliable access to clinical and business systems.
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from tools import (
    search_enterprise_knowledge,
    create_service_ticket,
    check_policy,
    escalate_to_human,
)
from config import IT_SUPPORT_MODEL

it_support_agent = LlmAgent(
    name="ITSupportAgent",
    model=LiteLlm(model=f"gemini/{IT_SUPPORT_MODEL}"),
    description=(
        "Answers IT support questions and creates IT service tickets for access, "
        "hardware, software, and system issues."
    ),
    instruction="""
        You are the IT Support Agent. You answer questions about password resets,
        laptop requests, access issues, software installation, VPN, MFA, and other
        enterprise IT services.

        Instructions:
        1. Use search_enterprise_knowledge with allowed_sources="it_support" to ground
           your answer in approved IT knowledge articles.
        2. Always cite the source document for every claim.
        3. For requests that need a ticket, use create_service_ticket(
           system="IT", summary, description, priority).
        4. If the tool returns status "error" or "blocked", report it clearly.
        5. For access to clinical or member-facing systems, use check_policy first.
        6. For system outages or security incidents, escalate_to_human("IT", summary, reason).
        7. Never provide instructions that bypass security controls (e.g. disable MFA).
        8. Do not request or display passwords, credentials, or PHI.

        Format: answer first, then sources.
    """,
    tools=[
        search_enterprise_knowledge,
        create_service_ticket,
        check_policy,
        escalate_to_human,
    ],
)
