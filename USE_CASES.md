# HR Use Cases — Enterprise Multi-Agent Assistant

This document maps the most common HR problems in large organizations to the agents,
tools, and workflows in this solution. Use it for stakeholder conversations, demo
scripts, and implementation prioritization.

---

## 1. High Volume of Repeat Questions

**Problem:** Employees ask the same HR, benefits, and payroll questions repeatedly.

**Business Impact:** HR teams spend time on low-value queries; employees wait for answers.

**Solution:**
- Self-service knowledge base search
- AI assistant with RAG-grounded answers
- FAQ chatbot

**Agent / Tool Mapping:**
| Capability | Agent | Tool |
|---|---|---|
| Route question to the right domain | RouterAgent | — |
| Answer HR policy questions | HRPolicyAgent | `search_enterprise_knowledge` |
| Answer benefits questions | BenefitsAgent | `search_enterprise_knowledge` |
| Answer payroll questions | PayrollAgent | `search_enterprise_knowledge` |

**Example Query:**
> "How many PTO days do I have?"

---

## 2. Slow Response Times

**Problem:** Employees wait days for HR case resolution.

**Business Impact:** Frustration, reduced productivity, and escalations.

**Solution:**
- Automated triage
- Case management with SLAs
- Instant answers for common questions

**Agent / Tool Mapping:**
| Capability | Agent | Tool |
|---|---|---|
| Create HR case | HRPolicyAgent, BenefitsAgent, PayrollAgent | `create_hr_case` |
| Create service ticket | ProcurementAgent, LegalAgent, ComplianceAgent, FacilitiesAgent | `create_service_ticket` |
| Escalate urgent cases | All specialists | `escalate_to_human` |

**Example Query:**
> "My paycheck was wrong. Can you open a payroll case?"

---

## 3. Inconsistent Answers

**Problem:** Different HR reps give different answers, creating confusion and compliance risk.

**Business Impact:** Policy violations, employee mistrust, audit findings.

**Solution:**
- Single source of truth for policies
- RAG-grounded answers with citations
- Standardized response templates

**Agent / Tool Mapping:**
| Capability | Agent | Tool |
|---|---|---|
| Grounded answers with citations | All specialist agents | `search_enterprise_knowledge` |
| Source documents | All specialist agents | `data/policies/` |

**Example Query:**
> "What is the parental leave policy?"

---

## 4. Onboarding Bottlenecks

**Problem:** New hires face delays in access, paperwork, and training.

**Business Impact:** Time-to-productivity increases, negative first impression.

**Solution:**
- Structured onboarding workflows
- Automated provisioning requests
- New-hire knowledge portal

**Agent / Tool Mapping:**
| Capability | Agent | Tool |
|---|---|---|
| Answer onboarding questions | HRPolicyAgent, ComplianceAgent | `search_enterprise_knowledge` |
| Check training eligibility | ComplianceAgent | `get_employee_eligibility` |
| Create onboarding case | HRPolicyAgent | `create_hr_case` |

**Example Query:**
> "What compliance training do I need to complete in my first 30 days?"

---

## 5. Benefits Confusion

**Problem:** Employees don't understand medical, dental, 401(k), enrollment windows, or eligibility.

**Business Impact:** Missed enrollment, poor benefits utilization, support spikes.

**Solution:**
- Benefits decision-support
- Personalized eligibility lookup
- Enrollment guides

**Agent / Tool Mapping:**
| Capability | Agent | Tool |
|---|---|---|
| Answer benefits questions | BenefitsAgent | `search_enterprise_knowledge` |
| Check eligibility | BenefitsAgent | `get_employee_eligibility` |
| Create benefits case | BenefitsAgent | `create_hr_case` |

**Example Query:**
> "Am I eligible for the 401(k) match?"

---

## 6. Payroll Errors and Disputes

**Problem:** Incorrect pay, missing deductions, or tax withholding issues.

**Business Impact:** Employee financial stress, legal exposure, payroll team workload.

**Solution:**
- Payroll case management
- Self-service paystub and tax forms
- Clear payroll policies

**Agent / Tool Mapping:**
| Capability | Agent | Tool |
|---|---|---|
| Answer payroll questions | PayrollAgent | `search_enterprise_knowledge` |
| Check payroll eligibility | PayrollAgent | `get_employee_eligibility` |
| Create payroll case | PayrollAgent | `create_hr_case` |
| Escalate sensitive dispute | PayrollAgent | `escalate_to_human` |

**Example Query:**
> "My W2 shows the wrong state. How do I fix it?"

---

## 7. Leave and Absence Management

**Problem:** Employees unsure about PTO, parental leave, sick leave, FMLA, or disability.

**Business Impact:** Absence abuse, manager confusion, compliance gaps.

**Solution:**
- Leave management system
- Self-service leave balances
- Clear parental and medical leave policies

**Agent / Tool Mapping:**
| Capability | Agent | Tool |
|---|---|---|
| Answer leave policy questions | HRPolicyAgent | `search_enterprise_knowledge` |
| Check leave eligibility | HRPolicyAgent | `get_employee_eligibility` |
| Create leave case | HRPolicyAgent | `create_hr_case` |

**Example Query:**
> "How do I request parental leave?"

---

## 8. Compliance and Training Tracking

**Problem:** Employees miss mandatory training; compliance gaps create audit risk.

**Business Impact:** Regulatory fines, audit findings, operational risk.

**Solution:**
- Learning management system integration
- Automated reminders
- Compliance dashboards

**Agent / Tool Mapping:**
| Capability | Agent | Tool |
|---|---|---|
| Answer training questions | ComplianceAgent | `search_enterprise_knowledge` |
| Check training eligibility | ComplianceAgent | `get_employee_eligibility` |
| Create compliance ticket | ComplianceAgent | `create_service_ticket` |

**Example Query:**
> "What compliance training is required for my role?"

---

## 9. Employee Relations and Escalations

**Problem:** Harassment, discrimination, grievances, or whistleblower reports need careful handling.

**Business Impact:** Legal risk, reputational damage, employee harm.

**Solution:**
- Anonymous ethics hotline
- Structured escalation workflows
- Human-in-the-loop for sensitive cases

**Agent / Tool Mapping:**
| Capability | Agent | Tool |
|---|---|---|
| Escalate sensitive topic | HRPolicyAgent, LegalAgent, ComplianceAgent | `escalate_to_human` |
| Route to right team | RouterAgent | — |

**Example Query:**
> "I need to report a workplace concern confidentially."

---

## 10. Performance and Talent Management

**Problem:** Inconsistent performance reviews, unclear goals, poor career visibility.

**Business Impact:** Disengagement, attrition, unclear development paths.

**Solution:**
- Performance management platform
- Goal-setting frameworks
- Career path documentation

**Agent / Tool Mapping:**
| Capability | Agent | Tool |
|---|---|---|
| Answer performance policy questions | HRPolicyAgent | `search_enterprise_knowledge` |
| Create HR case | HRPolicyAgent | `create_hr_case` |

**Example Query:**
> "When is the annual performance review cycle?"

---

## 11. Workforce Data and Reporting

**Problem:** HR data is scattered; leaders cannot make decisions.

**Business Impact:** Reactive HR, poor workforce planning.

**Solution:**
- HR analytics dashboard
- Centralized HRIS
- People analytics

**Agent / Tool Mapping:**
| Capability | Agent | Tool |
|---|---|---|
| Answer reporting policy questions | ComplianceAgent, HRPolicyAgent | `search_enterprise_knowledge` |
| Escalate data request | All specialists | `escalate_to_human` |

**Example Query:**
> "Who can request a workforce report?"

---

## 12. Policy Distribution and Acknowledgment

**Problem:** Employees don't read or acknowledge updated policies.

**Business Impact:** Non-compliance, disputes over policy awareness.

**Solution:**
- Policy acknowledgment workflows
- Annual attestations
- Searchable policy portal

**Agent / Tool Mapping:**
| Capability | Agent | Tool |
|---|---|---|
| Find and explain policies | All specialist agents | `search_enterprise_knowledge` |
| Cite specific documents | All specialist agents | `data/policies/` |

**Example Query:**
> "What is the remote work policy?"

---

## 13. Hybrid / Remote Work Challenges

**Problem:** Employees unsure about remote work eligibility, equipment, office access, or expenses.

**Business Impact:** Equipment delays, facilities confusion, policy inconsistency.

**Solution:**
- Remote work policy
- Equipment request workflows
- Facilities ticket system
- Expense reimbursement policies

**Agent / Tool Mapping:**
| Capability | Agent | Tool |
|---|---|---|
| Answer remote work policy | HRPolicyAgent | `search_enterprise_knowledge` |
| Equipment / facilities request | FacilitiesAgent | `create_service_ticket` |
| Procurement request | ProcurementAgent | `create_service_ticket` |

**Example Query:**
> "How do I request a new laptop?"

---

## 14. Recruitment and Hiring Delays

**Problem:** Slow hiring, poor candidate experience, manager frustration.

**Business Impact:** Lost candidates, team understaffing.

**Solution:**
- Applicant tracking system
- Structured interview guides
- Manager hiring dashboards

**Agent / Tool Mapping:**
| Capability | Agent | Tool |
|---|---|---|
| Answer hiring process questions | HRPolicyAgent | `search_enterprise_knowledge` |
| Create recruitment case | HRPolicyAgent | `create_hr_case` |

**Example Query:**
> "What is the approval process for opening a new req?"

---

## 15. Offboarding and Exit Management

**Problem:** Access not revoked, knowledge loss, or incomplete exit process.

**Business Impact:** Security risk, data loss, compliance issues.

**Solution:**
- Automated offboarding checklist
- Access revocation integrations
- Exit interviews

**Agent / Tool Mapping:**
| Capability | Agent | Tool |
|---|---|---|
| Answer offboarding questions | HRPolicyAgent | `search_enterprise_knowledge` |
| Create offboarding case | HRPolicyAgent | `create_hr_case` |
| Facilities access return | FacilitiesAgent | `create_service_ticket` |

**Example Query:**
> "What is the offboarding checklist?"

---

## Summary Mapping

| HR Problem | Primary Agent | Primary Tool |
|---|---|---|
| Repeat questions | RouterAgent | `search_enterprise_knowledge` |
| Slow response | All specialists | `create_hr_case` / `create_service_ticket` |
| Inconsistent answers | All specialists | `search_enterprise_knowledge` |
| Onboarding | ComplianceAgent, HRPolicyAgent | `get_employee_eligibility` |
| Benefits confusion | BenefitsAgent | `get_employee_eligibility` |
| Payroll disputes | PayrollAgent | `create_hr_case` |
| Leave management | HRPolicyAgent | `create_hr_case` |
| Compliance training | ComplianceAgent | `get_employee_eligibility` |
| Sensitive escalations | HRPolicyAgent, LegalAgent, ComplianceAgent | `escalate_to_human` |
| Performance management | HRPolicyAgent | `search_enterprise_knowledge` |
| Workforce reporting | ComplianceAgent | `escalate_to_human` |
| Policy distribution | All specialists | `search_enterprise_knowledge` |
| Remote work / equipment | FacilitiesAgent, ProcurementAgent | `create_service_ticket` |
| Recruitment | HRPolicyAgent | `create_hr_case` |
| Offboarding | HRPolicyAgent | `create_hr_case` |
