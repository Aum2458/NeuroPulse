import random
from typing import List, Dict, Optional

# -------------------- LIFESTYLE TIPS --------------------
lifestyle_tips: List[Dict[str, str]] = [
    {"tip": "Drink at least 8 glasses of water daily to stay hydrated.", "category": "Hydration"},
    {"tip": "Aim for 7–9 hours of quality sleep every night.", "category": "Sleep"},
    {"tip": "Include fresh fruits and vegetables in every meal.", "category": "Nutrition"},
    {"tip": "Do 30 minutes of moderate exercise at least 5 times a week.", "category": "Fitness"},
    {"tip": "Practice deep breathing or meditation for stress relief.", "category": "Mental Health"},
    {"tip": "Avoid excessive screen time before bedtime.", "category": "Sleep"},
    {"tip": "Maintain a consistent sleep-wake schedule.", "category": "Sleep"},
    {"tip": "Cut down on processed sugar and high-sodium snacks.", "category": "Nutrition"},
    {"tip": "Take regular breaks when working or studying.", "category": "Mental Health"},
    {"tip": "Build a daily habit journal to track progress and reflect.", "category": "Mindfulness"},
    {"tip": "Stretch every morning to improve flexibility and circulation.", "category": "Fitness"},
    {"tip": "Spend at least 20 minutes outdoors daily for fresh air and sunlight.", "category": "Well-being"}
]

# -------------------- FUNCTIONS --------------------

def get_lifestyle_tips(n: int = 5, category: Optional[str] = None) -> List[str]:
    """
    Returns up to 'n' lifestyle tips, optionally filtered by category.

    Args:
        n (int): Number of tips to return.
        category (str, optional): Category to filter tips by.

    Returns:
        List[str]: List of lifestyle tips.
    """
    filtered = [tip["tip"] for tip in lifestyle_tips if category is None or tip["category"].lower() == category.lower()]
    if not filtered:
        return [f"No tips found for category: {category}"]
    return random.sample(filtered, min(n, len(filtered)))


def get_grouped_lifestyle_tips() -> Dict[str, List[str]]:
    """
    Returns all lifestyle tips grouped by category.

    Returns:
        Dict[str, List[str]]: Dictionary where keys are categories and values are lists of tips.
    """
    grouped: Dict[str, List[str]] = {}
    for item in lifestyle_tips:
        grouped.setdefault(item["category"], []).append(item["tip"])
    return grouped


# -------------------- LOCAL TEST --------------------
if __name__ == "__main__":
    print("✅ Random Tips:\n", get_lifestyle_tips())
    print("\n💪 Fitness Tips Only:\n", get_lifestyle_tips(3, category="Fitness"))
    print("\n📚 Grouped Tips:\n", get_grouped_lifestyle_tips())
