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
from agents.purchasing_agent import purchasing_agent
from agents.legal_agent import legal_agent
from agents.compliance_agent import compliance_agent
from agents.facilities_agent import facilities_agent
from agents.it_support_agent import it_support_agent
from agents.provider_operations_agent import provider_operations_agent

router_agent = LlmAgent(
    name="RouterAgent",
    model=LiteLlm(model=f"gemini/{ROUTER_MODEL}"),
    description=(
        "Classifies enterprise service requests across HR, benefits, payroll, IT, "
        "procurement, purchasing, legal, compliance, facilities, and provider operations, "
        "then delegates to the right specialist agent."
    ),
    instruction="""
        You are the Enterprise Service Assistant Router. Your only job is to classify the
        request and route it to the correct specialist agent.

        Routing rules:
        - PTO, vacation, sick leave, parental leave, leave of absence, HR policies
          -> HRPolicyAgent
        - Medical, dental, vision, 401k, retirement, insurance, wellness
          -> BenefitsAgent
        - Paycheck, salary, deductions, W2, tax withholding, direct deposit
          -> PayrollAgent
        - Password reset, laptop, software install, access, VPN, MFA, system outage
          -> ITSupportAgent
        - Vendor, purchase order, invoice, procurement strategy, sourcing, expense, reimbursement
          -> ProcurementAgent
        - Buy something, purchase requisition, approval threshold, purchasing policy, purchase order status
          -> PurchasingAgent
        - Contract, NDA, legal review, IP, employment agreement, terms
          -> LegalAgent
        - Policy, audit, training, certification, compliance, ethics
          -> ComplianceAgent
        - Badge, building access, office, room, parking, maintenance, mail
          -> FacilitiesAgent
        - Provider onboarding, credentialing, provider contracts, directory updates,
          data submissions, provider operations
          -> ProviderOperationsAgent

        IMPORTANT healthcare guardrails:
        - If the request mentions a patient, member, diagnosis, treatment, or clinical
          decision, do NOT answer it. Route to ProviderOperationsAgent, which will escalate
          to a human. This platform is an enterprise service assistant, not a clinical agent.
        - If the request is sensitive (termination, harassment, whistleblower, medical
          accommodation), route to the appropriate specialist with an explicit note to
          escalate_to_human.

        If a request spans multiple domains, pick the most relevant specialist or ask a
        clarifying question. Always tell the user which specialist is handling the request.
        Do not answer the question yourself.
    """,
    sub_agents=[
        hr_policy_agent,
        benefits_agent,
        payroll_agent,
        it_support_agent,
        procurement_agent,
        purchasing_agent,
        legal_agent,
        compliance_agent,
        facilities_agent,
        provider_operations_agent,
    ],
)