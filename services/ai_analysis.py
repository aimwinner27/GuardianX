def analyze_report_urgency(description: str) -> str:
    """
    Very lightweight mock AI natural language processing 
    to classify urgency of suspicious activity reports.
    """
    description = description.lower()
    
    critical_keywords = ["weapon", "gun", "knife", "shooting", "bomb", "blood", "fire"]
    high_keywords = ["fight", "bullying", "drugs", "stealing", "theft", "screaming", "argument"]
    
    for word in critical_keywords:
        if word in description:
            return "critical"
            
    for word in high_keywords:
        if word in description:
            return "high"
            
    return "normal"
