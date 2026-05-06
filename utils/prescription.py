from fpdf import FPDF
from datetime import datetime
import os
import re
from typing import Optional
from .voice_utils import capture_symptom_voice

# -------------------------------------------------
# Constants
# -------------------------------------------------
PRESCRIPTION_DIR = "static/reports"

# -------------------------------------------------
# Utilities
# -------------------------------------------------
def sanitize_text(text: Optional[str]) -> str:
    """
    Removes emojis / unsupported characters for PDF safety.
    """
    if not text:
        return "No content provided."
    return re.sub(r"[^\x00-\x7F]+", "", str(text))

# -------------------------------------------------
# PDF Generator
# -------------------------------------------------
def generate_prescription_from_voice(username: str) -> str:
    """
    Captures voice input and generates a prescription-style PDF.

    Args:
        username (str): Patient username

    Returns:
        str: Relative path to generated PDF
    """
    os.makedirs(PRESCRIPTION_DIR, exist_ok=True)

    # Capture voice input
    spoken_text = capture_symptom_voice()
    spoken_text = sanitize_text(spoken_text)

    # File naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"voice_prescription_{username}_{timestamp}.pdf"
    file_path = os.path.join(PRESCRIPTION_DIR, filename)

    # Initialize PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # -----------------------------
    # Header
    # -----------------------------
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "NeuroPulse-MDx+ | Voice Prescription", ln=True, align="C")
    pdf.ln(8)

    # -----------------------------
    # Patient Details
    # -----------------------------
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Patient Username: {username}", ln=True)
    pdf.cell(0, 8, f"Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", ln=True)
    pdf.ln(8)

    # -----------------------------
    # Prescription Content
    # -----------------------------
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "Voice Captured Notes:", ln=True)
    pdf.ln(2)

    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, spoken_text)
    pdf.ln(6)

    # -----------------------------
    # Disclaimer
    # -----------------------------
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(
        0,
        7,
        "Disclaimer: This document is generated from voice input using an AI-assisted system. "
        "It is intended for reference only and does not constitute a medical prescription. "
        "Always consult a licensed medical professional before taking any medication."
    )

    # Reset color
    pdf.set_text_color(0, 0, 0)

    # Save PDF
    pdf.output(file_path)

    return file_path
