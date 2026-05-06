from typing import List, Dict

def get_ai_chart_data(risk_dict: Dict[str, int]) -> List[Dict[str, float]]:
    """
    Converts risk-level counts dictionary into Chart.js-friendly format.

    Args:
        risk_dict (dict): Example:
            {
                "LOW": 5,
                "MODERATE": 3,
                "CRITICAL": 1
            }

    Returns:
        list: Example:
            [
                {"label": "Critical", "value": 1.0},
                {"label": "Moderate", "value": 3.0},
                {"label": "Low", "value": 5.0}
            ]
        Sorted by severity descending (CRITICAL first).
    """
    if not isinstance(risk_dict, dict):
        return []

    chart_data = []
    severity_order = ["CRITICAL", "MODERATE", "LOW"]  # CRITICAL first

    for level in severity_order:
        value = risk_dict.get(level, 0)
        chart_data.append({
            "label": level.title(),   # Capitalize for display
            "value": float(value)
        })

    return chart_data
