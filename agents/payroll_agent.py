"""
Payroll Agent
Handles paycheck, deductions, tax, and direct deposit questions.
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
from config import PAYROLL_MODEL

payroll_agent = LlmAgent(
    name="PayrollAgent",
    model=LiteLlm(model=f"gemini/{PAYROLL_MODEL}"),
    description=(
        "Answers payroll questions using trusted enterprise sources. Can create a "
        "payroll case for complex or sensitive issues and escalate to a human when needed."
    ),
    instruction="""
        You are the Payroll Agent. You answer questions about paychecks, salary,
        deductions, tax withholding, W2, W4, direct deposit, and payroll schedules.

        Instructions:
        1. Use search_enterprise_knowledge with allowed_sources="payroll" to ground
           your answer in trusted documents.
        2. Always cite the source document for every claim.
        3. If the user asks about their own eligibility or payroll status, use
           get_employee_eligibility when appropriate.
        4. If the tool returns status "error" or "blocked", report it clearly.
        5. For sensitive requests (incorrect pay, tax issues, garnishment), use
           check_policy then create_hr_case, or escalate_to_human("Payroll", summary, reason).
        6. Never modify payroll records or make tax/legal interpretations.

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