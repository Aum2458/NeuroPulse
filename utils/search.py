from typing import List, Dict, Any, Optional
import re

# -------------------------------------------------
# Static Health Knowledge Base
# (Can later be replaced with a DB or API)
# -------------------------------------------------
KNOWLEDGE_BASE: List[Dict[str, str]] = [
    {"title": "Diabetes Management", "description": "How to manage diabetes through diet, exercise, blood sugar monitoring, and medication."},
    {"title": "Hypertension Guide", "description": "Information about high blood pressure, causes, symptoms, and control measures."},
    {"title": "Mental Health Support", "description": "Counseling options, therapy types, stress management, and emotional well-being."},
    {"title": "Heart Disease Prevention", "description": "Lifestyle changes, diet plans, and physical activity to prevent heart problems."},
    {"title": "COVID-19 Recovery", "description": "Post-COVID symptoms, rest guidelines, breathing exercises, and doctor consultation."},
    {"title": "Vaccination Schedule", "description": "Recommended immunizations by age, medical condition, and risk category."},
    {"title": "Nutrition Basics", "description": "Essential vitamins, minerals, balanced diet tips, and healthy eating habits."},
    {"title": "Sleep Hygiene", "description": "How to improve sleep quality, manage insomnia, and maintain sleep routines."},
    {"title": "Asthma Support", "description": "Managing asthma triggers, inhaler usage, and long-term control strategies."},
    {"title": "Stress Relief Techniques", "description": "Breathing exercises, mindfulness practices, and relaxation techniques."}
]

# -------------------------------------------------
# Utility
# -------------------------------------------------
def normalize(text: str) -> str:
    """Normalize text for safe comparison (lowercase, strip spaces)."""
    return re.sub(r"\s+", " ", text.lower().strip())

# -------------------------------------------------
# Smart Search Engine
# -------------------------------------------------
def smart_search(query: Optional[str]) -> List[Dict[str, Any]]:
    """
    Performs a keyword-based search over the health knowledge base.

    Args:
        query (str): User search input

    Returns:
        List[Dict[str, Any]]: Ranked matching results by relevance
    """
    if not query or not query.strip():
        return []

    query_norm = normalize(query)
    results: List[Dict[str, Any]] = []

    for entry in KNOWLEDGE_BASE:
        title = normalize(entry.get("title", ""))
        description = normalize(entry.get("description", ""))

        # Simple relevance scoring
        score = 0
        if query_norm in title:
            score += 2
        if query_norm in description:
            score += 1

        if score > 0:
            results.append({
                "title": entry["title"],
                "description": entry["description"],
                "relevance": score
            })

    # Sort by relevance (descending)
    results.sort(key=lambda x: x["relevance"], reverse=True)

    return results

# -------------------- LOCAL TEST --------------------
if __name__ == "__main__":
    query = "diabetes"
    matches = smart_search(query)
    print(f"Search results for '{query}':\n")
    for m in matches:
        print(f"- {m['title']} (Score: {m['relevance']})")
        print(f"  {m['description']}\n")
