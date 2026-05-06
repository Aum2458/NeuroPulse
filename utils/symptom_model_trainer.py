import os
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request, redirect,
    session, url_for, jsonify, send_file, flash
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import joblib

# ---------- App Config ----------
app = Flask(__name__)
app.secret_key = "admin_secret_key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
AI_DIR = os.path.join(BASE_DIR, "ai")
REPORT_DIR = os.path.join(BASE_DIR, "static/reports")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///neuro_pulse.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------- Load AI Models ----------
model = joblib.load(os.path.join(AI_DIR, "disease_model.pkl"))
vectorizer = joblib.load(os.path.join(AI_DIR, "vectorizer.pkl"))

# ---------- Import Utilities ----------
from gemini_ai import paraphrase_symptoms
from qr import generate_qr
from search import smart_search

# ---------- Database Models ----------
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, default=0.0)
    report_file = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------- Auth Decorator ----------
def admin_login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "admin_id" not in session:
            flash("Please log in first.", "danger")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return wrapper

# ---------- Admin Login ----------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"].strip().lower()
        password = request.form["password"]

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session["admin_id"] = admin.id
            session["admin_username"] = admin.username
            flash("Login successful.", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Invalid credentials.", "danger")
    return render_template("admin/login.html")

# ---------- Logout ----------
@app.route("/admin/logout")
@admin_login_required
def admin_logout():
    session.pop("admin_id", None)
    session.pop("admin_username", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("admin_login"))

# ---------- Admin Dashboard ----------
@app.route("/admin/dashboard")
@admin_login_required
def admin_dashboard():
    patients = Patient.query.order_by(Patient.created_at.desc()).all()
    total = Patient.query.count()
    return render_template(
        "admin/dashboard.html",
        patients=patients,
        total=total
    )

# ---------- AI Diagnosis ----------
@app.route("/admin/diagnose", methods=["POST"])
@admin_login_required
def diagnose():
    name = request.form.get("name", "").strip()
    symptoms = request.form.get("symptoms", "").strip()

    if not name or not symptoms:
        return jsonify({"error": "Name and symptoms are required"}), 400

    # Paraphrase / clarify symptoms via Gemini AI
    clean_symptoms = paraphrase_symptoms(symptoms)

    try:
        vect = vectorizer.transform([clean_symptoms])
        prediction = model.predict(vect)[0]
        confidence = max(model.predict_proba(vect)[0]) * 100  # percentage
    except Exception as e:
        return jsonify({"error": f"AI prediction failed: {e}"}), 500

    patient = Patient(
        name=name,
        symptoms=clean_symptoms,
        diagnosis=prediction,
        confidence=round(confidence, 2)
    )
    db.session.add(patient)
    db.session.commit()

    return jsonify({
        "name": name,
        "diagnosis": prediction,
        "confidence": round(confidence, 2)
    })

# ---------- Smart Knowledge Search ----------
@app.route("/admin/search")
@admin_login_required
def admin_search():
    query = request.args.get("q", "")
    results = smart_search(query)
    return jsonify(results)

# ---------- Report QR Generator ----------
@app.route("/admin/report/qr")
@admin_login_required
def report_qr():
    filename = request.args.get("file")
    if not filename:
        return jsonify({"error": "Filename required"}), 400

    file_path = os.path.join(REPORT_DIR, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File does not exist"}), 404

    qr_path = generate_qr(file_path)
    return jsonify({"qr": qr_path})

# ---------- Download Report ----------
@app.route("/admin/report/download/<filename>")
@admin_login_required
def download_report(filename):
    file_path = os.path.join(REPORT_DIR, filename)
    if not os.path.exists(file_path):
        flash("File not found.", "danger")
        return redirect(url_for("admin_dashboard"))
    return send_file(file_path, as_attachment=True)

# ---------- System Stats API ----------
@app.route("/admin/stats")
@admin_login_required
def stats():
    return jsonify({
        "patients": Patient.query.count(),
        "reports": len(os.listdir(REPORT_DIR)) if os.path.exists(REPORT_DIR) else 0,
        "ai_model": "Active",
        "system": "Online"
    })

# ---------- Init ----------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # ✅ Create default admin if none exists
        if not Admin.query.first():
            default_admin = Admin(username="admin")
            default_admin.set_password("admin123")  # Change after first login!
            db.session.add(default_admin)
            db.session.commit()
            print("Default admin created (username=admin, password=admin123)")

    app.run(debug=True)
