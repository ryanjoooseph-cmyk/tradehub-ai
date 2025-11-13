# reviewer_agent.py
from typing import Optional, Dict, Any

def review(output_text: str, feature: Optional[str] = None) -> Dict[str, Any]:
    """
    Minimal reviewer that always 'approves' so the pipeline can run.
    Upgrade later with real checks/tests.
    """
    return {
        "approved": True,
        "notes": "Auto-approved by stub reviewer.",
        "feature": feature,
        "summary_chars": len(output_text or ""),
    }