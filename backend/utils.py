"""
Simple contract analysis function for testing purposes.
This simulates the GDPR compliance analysis without requiring external dependencies.
"""

def analyze_contract(content):
    """
    Analyze a contract for GDPR compliance.
    
    Args:
        content (str): The contract content to analyze
        
    Returns:
        dict: Analysis results
    """
    # Simple keyword-based analysis for testing
    keywords = {
        "data controller": "Article 28(3)(a)",
        "data processor": "Article 28(3)(b)",
        "processing instructions": "Article 28(3)(c)",
        "confidentiality": "Article 28(3)(d)",
        "security measures": "Article 28(3)(e)",
        "sub-processing": "Article 28(3)(f)",
        "assistance": "Article 28(3)(g)",
        "deletion": "Article 28(3)(h)",
        "audit": "Article 28(3)(i)"
    }
    
    # Find matching keywords
    found_articles = []
    for keyword, article in keywords.items():
        if keyword.lower() in content.lower():
            found_articles.append({
                "article": article,
                "keyword": keyword,
                "found": True,
                "confidence": 0.95
            })
    
    # Always include some basic findings for testing
    compliance_issues = [
        {
            "id": "1",
            "article": "Article 28(3)(a)",
            "description": "Data controller identification",
            "status": "Present",
            "confidence": 0.95,
            "snippet": "This agreement outlines the data processing obligations between parties.",
            "recommendation": "Ensure clear identification of data controller and processor roles."
        },
        {
            "id": "2",
            "article": "Article 28(3)(d)",
            "description": "Confidentiality obligations",
            "status": "Missing",
            "confidence": 0.85,
            "snippet": "Personal data will be processed in accordance with GDPR requirements.",
            "recommendation": "Add specific confidentiality obligations for personnel authorized to process data."
        }
    ]
    
    # Generate coverage data
    coverage = []
    for keyword, article in keywords.items():
        present = keyword.lower() in content.lower()
        coverage.append({
            "article": article,
            "status": "Present" if present else "Missing",
            "confidence": 0.95 if present else 0.75,
            "present": present,
            "strength": "Strong" if present else "Weak"
        })
    
    return {
        "compliance_issues": compliance_issues,
        "coverage": coverage,
        "summary": {
            "total_articles": len(keywords),
            "articles_covered": len([c for c in coverage if c["present"]]),
            "compliance_score": len([c for c in coverage if c["present"]]) / len(keywords)
        }
    }