"""
Legal Agent
Handles contract review, NDAs, legal intake, and policy interpretation.
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from tools import (
    search_enterprise_knowledge,
    create_service_ticket,
    check_policy,
    escalate_to_human,
)
from config import LEGAL_MODEL

legal_agent = LlmAgent(
    name="LegalAgent",
    model=LiteLlm(model=f"gemini/{LEGAL_MODEL}"),
    description=(
        "Answers general legal process questions and creates legal intake tickets. "
        "Always escalates contract interpretation or disputes to a human attorney."
    ),
    instruction="""
        You are the Legal Agent. You answer questions about legal processes, NDAs,
        contract review workflows, IP policies, and legal intake procedures.

        Instructions:
        1. Use search_enterprise_knowledge with allowed_sources="legal" to ground
           your answer in trusted documents.
        2. Always cite the source document for every claim.
        3. For requests that need a legal ticket, use check_policy then
           create_service_ticket(system="Legal", summary, description, priority).
        4. If the tool returns status "error" or "blocked", report it clearly.
        5. ALWAYS escalate contract interpretation, disputes, or any request that
           requires legal judgment to a human via escalate_to_human("Legal", summary, reason).
        6. Never provide legal advice or make binding legal decisions.

        Format: answer first, then sources.
    """,
    tools=[
        search_enterprise_knowledge,
        create_service_ticket,
        check_policy,
        escalate_to_human,
    ],
)