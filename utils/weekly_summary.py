import os
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from typing import List, Dict, Any

# -------------------------
# Directories
# -------------------------
DATA_DIR = "static/timeline"
SUMMARY_DIR = "static/reports"

# -------------------------
# Weekly Summary Generator
# -------------------------
def generate_weekly_summary(username: str) -> str:
    """
    Generates a weekly health summary PDF from the last 5 timeline entries.

    Args:
        username (str): The user's username.

    Returns:
        str: Relative path to the saved PDF report (used for download/view).
    """
    os.makedirs(SUMMARY_DIR, exist_ok=True)
    timeline_file = os.path.join(DATA_DIR, f"{username}_timeline.json")
    summary_path = os.path.join(SUMMARY_DIR, f"weekly_summary_{username}.pdf")

    # -------------------------
    # Load timeline
    # -------------------------
    if not os.path.exists(timeline_file):
        raise FileNotFoundError(f"❌ No timeline data found for {username}.")

    with open(timeline_file, "r", encoding="utf-8") as f:
        timeline: List[Dict[str, Any]] = json.load(f)

    if not timeline:
        raise ValueError(f"⚠️ Timeline for {username} is empty.")

    # -------------------------
    # Initialize PDF
    # -------------------------
    c = canvas.Canvas(summary_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"🩺 Weekly Health Summary for {username}")
    c.setFont("Helvetica", 12)

    y = height - 80
    entries_to_show = timeline[:5]  # Most recent 5 entries

    for entry in entries_to_show:
        timestamp = entry.get('timestamp', 'N/A')
        symptoms = entry.get("symptoms", "N/A")
        result = entry.get("result", {})
        diagnosis = result.get("diagnosis", "N/A")
        ai_summary = result.get("ai_summary", "No summary provided.")

        # Write to PDF
        c.drawString(50, y, f"📅 {timestamp}")
        y -= 16
        c.drawString(70, y, f"Symptoms: {symptoms}")
        y -= 16
        c.drawString(70, y, f"Diagnosis: {diagnosis}")
        y -= 16
        c.drawString(70, y, f"AI Insight: {ai_summary}")
        y -= 28

        # New page if space runs out
        if y < 100:
            c.showPage()
            y = height - 80
            c.setFont("Helvetica", 12)

    c.save()
    print(f"✅ Weekly summary generated: {summary_path}")
    return summary_path


# -------------------------
# Quick Test
# -------------------------
if __name__ == "__main__":
    test_user = "test_patient"
    try:
        pdf_path = generate_weekly_summary(test_user)
        print(f"PDF saved at: {pdf_path}")
    except Exception as e:
        print(f"⚠️ Error generating summary: {e}")
