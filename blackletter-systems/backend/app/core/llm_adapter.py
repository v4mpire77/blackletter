"""
LLM adapter module for simulating contract analysis.
"""
import uuid
import random
from datetime import datetime
from typing import List, Optional

from models.schemas import Issue, IssueType, Severity


def analyze_contract_with_llm(contract_text: str, filename: Optional[str] = None) -> List[Issue]:
    """
    Simulate LLM-based analysis of contract text.
    
    Args:
        contract_text: The text content of the contract
        filename: Optional filename to influence simulation results
        
    Returns:
        List of simulated compliance issues found in the contract
    """
    # In a real implementation, this would call an actual LLM API
    # For simulation, we'll generate issues based on keywords in the text
    
    issues = []
    now = datetime.utcnow()
    
    # Check for common contract issues
    if "CONFIDENTIAL INFORMATION" in contract_text or "confidential" in contract_text.lower():
        issues.append(Issue(
            id=str(uuid.uuid4()),
            type=IssueType.IP_RIGHTS,
            title="Incomplete Confidentiality Clause",
            description="The confidentiality clause lacks specific remedies for breach.",
            severity=Severity.MEDIUM,
            clause="Section 5",
            page_number=1,
            remediation="Add specific remedies and liquidated damages for confidentiality breaches.",
            timestamp=now
        ))
    
    if "DATA PROTECTION" in contract_text or "data" in contract_text.lower():
        issues.append(Issue(
            id=str(uuid.uuid4()),
            type=IssueType.DATA_PROTECTION,
            title="Vague Data Protection Terms",
            description="Data protection provisions lack specificity on data types and processing purposes.",
            severity=Severity.HIGH,
            clause="Section 6",
            page_number=1,
            remediation="Specify data types, processing purposes, and retention periods explicitly.",
            timestamp=now
        ))
    
    if "GDPR" in contract_text or "gdpr" in contract_text.lower():
        issues.append(Issue(
            id=str(uuid.uuid4()),
            type=IssueType.GDPR,
            title="Missing Data Subject Rights",
            description="The contract doesn't address data subject rights under GDPR Article 15-22.",
            severity=Severity.HIGH,
            clause="Section 9",
            page_number=2,
            remediation="Add provisions for data subject access, rectification, erasure, and portability rights.",
            timestamp=now
        ))
    
    if "TERMINATION" in contract_text or "terminat" in contract_text.lower():
        issues.append(Issue(
            id=str(uuid.uuid4()),
            type=IssueType.EMPLOYMENT,
            title="Inadequate Notice Period",
            description="The termination notice period may not comply with local employment regulations.",
            severity=Severity.MEDIUM,
            clause="Section 7",
            page_number=1,
            remediation="Review and align termination notice period with local employment laws.",
            timestamp=now
        ))
    
    if "ENVIRONMENTAL" in contract_text or "environment" in contract_text.lower():
        issues.append(Issue(
            id=str(uuid.uuid4()),
            type=IssueType.ENVIRONMENTAL,
            title="Environmental Compliance Too General",
            description="Environmental compliance clause lacks specific requirements and reporting obligations.",
            severity=Severity.LOW,
            clause="Section 9",
            page_number=2,
            remediation="Add specific environmental compliance standards and regular reporting requirements.",
            timestamp=now
        ))
    
    if "COMPENSATION" in contract_text or "compensation" in contract_text.lower():
        issues.append(Issue(
            id=str(uuid.uuid4()),
            type=IssueType.EMPLOYMENT,
            title="Missing Bonus Structure Details",
            description="Compensation section lacks clear criteria for bonus eligibility and calculation.",
            severity=Severity.LOW,
            clause="Section 3",
            page_number=1,
            remediation="Add specific bonus eligibility criteria and calculation methods.",
            timestamp=now
        ))
    
    # Always add at least one random issue if none were found
    if not issues:
        random_types = [
            (IssueType.CONSUMER_RIGHTS, "Missing Cooling-off Period", "No consumer right to withdraw is specified within statutory timeframes."),
            (IssueType.TAX, "Tax Compliance Risk", "Contract lacks provisions for tax withholding requirements."),
            (IssueType.ANTI_MONEY_LAUNDERING, "AML Verification Missing", "No Anti-Money Laundering verification procedures specified."),
            (IssueType.COMPETITION_LAW, "Potential Anti-competitive Clause", "Exclusivity provisions may violate competition regulations.")
        ]
        
        random_choice = random.choice(random_types)
        issues.append(Issue(
            id=str(uuid.uuid4()),
            type=random_choice[0],
            title=random_choice[1],
            description=random_choice[2],
            severity=random.choice([Severity.LOW, Severity.MEDIUM, Severity.HIGH]),
            clause=f"Section {random.randint(1, 10)}",
            page_number=random.randint(1, 3),
            remediation=f"Review and revise according to {random_choice[0].value} regulations.",
            timestamp=now
        ))
    
    # Add a few more random issues occasionally to create variety
    if random.random() < 0.7:  # 70% chance to add more issues
        num_extra_issues = random.randint(1, 3)
        for _ in range(num_extra_issues):
            severity_choice = random.choice([Severity.LOW, Severity.MEDIUM, Severity.HIGH])
            type_choice = random.choice(list(IssueType))
            
            if type_choice == IssueType.EMPLOYMENT:
                issues.append(Issue(
                    id=str(uuid.uuid4()),
                    type=type_choice,
                    title="Working Hours Not Specified",
                    description="The contract does not clearly define working hours or overtime policy.",
                    severity=severity_choice,
                    clause=f"Section {random.randint(1, 10)}",
                    page_number=random.randint(1, 3),
                    remediation="Add specific working hours, days, and overtime compensation policy.",
                    timestamp=now
                ))
            elif type_choice == IssueType.GDPR:
                issues.append(Issue(
                    id=str(uuid.uuid4()),
                    type=type_choice,
                    title="Cross-border Data Transfer Issues",
                    description="The contract doesn't address international data transfer safeguards.",
                    severity=severity_choice,
                    clause=f"Section {random.randint(1, 10)}",
                    page_number=random.randint(1, 3),
                    remediation="Add standard contractual clauses for international data transfers.",
                    timestamp=now
                ))
            else:
                issues.append(Issue(
                    id=str(uuid.uuid4()),
                    type=type_choice,
                    title=f"Generic {type_choice.value.replace('_', ' ').title()} Issue",
                    description=f"This is a simulated {type_choice.value.replace('_', ' ')} compliance issue.",
                    severity=severity_choice,
                    clause=f"Section {random.randint(1, 10)}",
                    page_number=random.randint(1, 3),
                    remediation=f"Review and update according to relevant {type_choice.value.replace('_', ' ')} regulations.",
                    timestamp=now
                ))
    
    return issues
