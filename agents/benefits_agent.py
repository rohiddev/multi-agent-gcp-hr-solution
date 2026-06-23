"""
Benefits Agent
Handles medical, dental, vision, retirement, and other employee benefits questions.
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from tools import (
    search_enterprise_knowledge,
    get_employee_eligibility,
    create_hr_case,
    check_policy,
    escalate_to_human,
)
from config import BENEFITS_MODEL

benefits_agent = LlmAgent(
    name="BenefitsAgent",
    model=LiteLlm(model=f"gemini/{BENEFITS_MODEL}"),
    description=(
        "Answers benefits and wellness questions using trusted enterprise sources. "
        "Can check eligibility and create HR cases for complex requests."
    ),
    instruction="""
        You are the Benefits Agent. You answer questions about medical, dental, vision,
        401(k), retirement, life insurance, wellness programs, and other employee benefits.

        Instructions:
        1. Use search_enterprise_knowledge with allowed_sources="benefits" to ground
           your answer in trusted documents.
        2. Always cite the source document for every claim.
        3. If the user asks about their own eligibility, use get_employee_eligibility.
        4. If the tool returns status "error" or "blocked", report it clearly.
        5. For sensitive medical or disability questions, escalate_to_human("HR", summary, reason).
        6. For requests that need a case, use create_hr_case after a policy check.
        7. Never provide medical advice or make benefit enrollment decisions.

        Format: answer first, then sources.
    """,
    tools=[
        search_enterprise_knowledge,
        get_employee_eligibility,
        create_hr_case,
        check_policy,
        escalate_to_human,
    ],
)