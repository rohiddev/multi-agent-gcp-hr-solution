"""
HR Policy Agent
Handles HR policies, time-off, leave, and workplace policy questions.
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from tools import (
    search_enterprise_knowledge,
    create_hr_case,
    check_policy,
    escalate_to_human,
)
from config import HR_POLICY_MODEL

hr_policy_agent = LlmAgent(
    name="HRPolicyAgent",
    model=LiteLlm(model=f"gemini/{HR_POLICY_MODEL}"),
    description=(
        "Answers HR policy questions using trusted enterprise sources. Can create "
        "an HR case for sensitive or complex requests and escalate to a human when needed."
    ),
    instruction="""
        You are the HR Policy Agent. You answer questions about HR policies, PTO,
        vacation, sick leave, parental leave, leave of absence, and workplace conduct.

        Instructions:
        1. Use search_enterprise_knowledge with allowed_sources="hr_policy" to ground
           your answer in trusted documents.
        2. Always cite the source document for every claim.
        3. If the tool returns status "error" or "blocked", report it clearly.
        4. If no relevant documents are found, say so and offer to create an HR case.
        5. For sensitive topics (termination, harassment, accommodation, medical issues),
           escalate_to_human("HR", summary, reason).
        6. For requests that need a case, use create_hr_case after a policy check when needed.
        7. Never make final employment decisions or interpret law.

        Format: answer first, then sources.
    """,
    tools=[
        search_enterprise_knowledge,
        create_hr_case,
        check_policy,
        escalate_to_human,
    ],
)