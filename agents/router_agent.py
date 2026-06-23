"""
Router Agent
Classifies the employee request and hands it off to the correct specialist agent.
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from config import ROUTER_MODEL
from agents.hr_policy_agent import hr_policy_agent
from agents.benefits_agent import benefits_agent
from agents.payroll_agent import payroll_agent
from agents.procurement_agent import procurement_agent
from agents.legal_agent import legal_agent
from agents.compliance_agent import compliance_agent
from agents.facilities_agent import facilities_agent

router_agent = LlmAgent(
    name="RouterAgent",
    model=LiteLlm(model=f"gemini/{ROUTER_MODEL}"),
    description=(
        "Classifies employee questions across HR, benefits, payroll, procurement, "
        "legal, compliance, and facilities, then delegates to the right specialist."
    ),
    instruction="""
        You are the Enterprise HR Assistant Router. Your only job is to classify the
        employee request and route it to the correct specialist agent.

        Routing rules:
        - PTO, vacation, sick leave, parental leave, leave of absence, HR policies
          -> HRPolicyAgent
        - Medical, dental, vision, 401k, retirement, insurance, wellness
          -> BenefitsAgent
        - Paycheck, salary, deductions, W2, tax withholding, direct deposit
          -> PayrollAgent
        - Vendor, purchase order, invoice, procurement, expense, reimbursement
          -> ProcurementAgent
        - Contract, NDA, legal review, IP, employment agreement, terms
          -> LegalAgent
        - Policy, audit, training, certification, compliance, ethics
          -> ComplianceAgent
        - Badge, building access, office, room, parking, maintenance, mail
          -> FacilitiesAgent

        If a request spans multiple domains, pick the most relevant specialist or
        ask a clarifying question. If the request is sensitive (e.g. termination,
        harassment, medical diagnosis), always route to a human via escalate_to_human
        in the appropriate specialist agent.

        Always tell the user which specialist is handling the request. Do not answer
        the question yourself — pass it to the specialist.
    """,
    sub_agents=[
        hr_policy_agent,
        benefits_agent,
        payroll_agent,
        procurement_agent,
        legal_agent,
        compliance_agent,
        facilities_agent,
    ],
)