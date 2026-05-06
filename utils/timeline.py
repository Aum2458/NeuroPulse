import json
import os
from datetime import datetime
from typing import List, Dict, Any

# -------------------------------------------------
# Directory to store all patient timelines
# -------------------------------------------------
TIMELINE_DIR = "static/timeline"


def _get_timeline_path(username: str) -> str:
    """
    Returns the full path of a patient's timeline file.
    Ensures the directory exists.
    """
    os.makedirs(TIMELINE_DIR, exist_ok=True)
    safe_username = username.lower().replace(" ", "_")
    return os.path.join(TIMELINE_DIR, f"{safe_username}_timeline.json")


def update_timeline(username: str, symptoms: str, result: Dict[str, Any]) -> None:
    """
    Adds a new diagnosis record to the patient's timeline.

    Args:
        username (str): Patient identifier
        symptoms (str): Symptoms entered by patient
        result (Dict): Diagnosis result (AI output, suggestions, etc.)
    """
    path = _get_timeline_path(username)
    timeline: List[Dict[str, Any]] = []

    # Load existing timeline safely
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                timeline = json.load(f)
        except (json.JSONDecodeError, IOError):
            timeline = []

    # New timeline entry
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symptoms": symptoms,
        "result": result
    }

    # Insert newest record first
    timeline.insert(0, entry)

    # Optional: keep last 50 records only
    timeline = timeline[:50]

    # Save timeline safely
    try:
        with open(path, "w") as f:
            json.dump(timeline, f, indent=2)
    except IOError as e:
        print(f"⚠️ Failed to save timeline for {username}: {e}")


def get_patient_timeline(username: str) -> List[Dict[str, Any]]:
    """
    Retrieves the patient's diagnosis timeline.

    Args:
        username (str): Patient identifier

    Returns:
        List[Dict[str, Any]]: Timeline history (newest first)
    """
    path = _get_timeline_path(username)

    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    return []
