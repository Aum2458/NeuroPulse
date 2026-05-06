from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from datetime import datetime, timedelta
import random
import os

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# =====================================================
# 📊 Weekly Diagnosis Statistics (Dummy Data)
# NOTE: Replace with database queries later
# =====================================================
def get_weekly_diagnosis_stats():
    """
    Simulates weekly diagnosis activity for admin analytics.
    This does NOT represent real medical accuracy.
    """
    today = datetime.now()
    stats = []

    for i in range(7):
        day = today - timedelta(days=6 - i)
        stats.append({
            "date": day.strftime("%a"),
            "count": random.randint(3, 15)  # simulated system usage
        })

    return stats


# =====================================================
# 🧑‍💼 Admin Dashboard View
# =====================================================
@admin_bp.route("/dashboard")
def admin_dashboard():
    """
    Admin analytics dashboard:
    - Weekly system usage
    - Reports & monitoring
    """
    chart_data = get_weekly_diagnosis_stats()

    return render_template(
        "admin_dashboard.html",
        chart_data=chart_data
    )


# =====================================================
# 🔐 OTP Generation (Family / Emergency Access)
# =====================================================
@admin_bp.route("/generate-otp", methods=["POST"])
def generate_otp():
    """
    Generates a temporary OTP.
    In production, OTP should be emailed or SMSed.
    """
    email = request.form.get("email")

    if not email:
        flash("Email is required to generate OTP", "danger")
        return redirect(url_for("admin.admin_dashboard"))

    otp = random.randint(100000, 999999)

    # 🚨 DEMO ONLY (no real email service)
    print(f"[DEMO OTP] Email: {email}, OTP: {otp}")

    flash("OTP generated successfully (demo mode)", "success")
    return redirect(url_for("admin.admin_dashboard"))


# =====================================================
# 📄 Weekly PDF Admin Report
# =====================================================
@admin_bp.route("/generate-weekly-report")
def generate_weekly_report():
    """
    Generates a PDF summary of weekly system activity.
    """
    from fpdf import FPDF

    reports_dir = "static/reports"
    os.makedirs(reports_dir, exist_ok=True)

    filename = f"weekly_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = os.path.join(reports_dir, filename)

    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "NeuroPulse-MDx+ Weekly Admin Report", ln=True, align="C")
    pdf.ln(8)

    # Meta
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", ln=True)
    pdf.ln(6)

    # Content
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, "System Activity Summary", ln=True)
    pdf.ln(4)

    pdf.set_font("Arial", "", 12)
    for day in get_weekly_diagnosis_stats():
        pdf.cell(0, 8, f"{day['date']} : {day['count']} symptom checks", ln=True)

    # Disclaimer
    pdf.ln(8)
    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(
        0,
        8,
        "Disclaimer: This report is generated for administrative monitoring only. "
        "It does not represent medical diagnosis or patient treatment data."
    )

    pdf.output(path)

    return send_file(path, as_attachment=True)
