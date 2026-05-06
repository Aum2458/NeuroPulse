from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from datetime import datetime
import os

# ✅ IMPORT DB
from db import db, init_db, User

# ---------------- SETUP ----------------
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "safe_dev_key")

# ✅ NEW DATABASE NAME
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///neuro_pulse_v3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

socketio = SocketIO(app)

# ---------------- MODELS ----------------
class PatientRecord(db.Model):
    __tablename__ = "patient_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    symptoms = db.Column(db.String(200))
    severity = db.Column(db.String(20))
    duration = db.Column(db.Integer)
    age = db.Column(db.Integer)
    bp = db.Column(db.String(20))

    spo2 = db.Column(db.Integer, nullable=True)  # optional

    sugar = db.Column(db.Integer)
    pain = db.Column(db.Integer)
    city = db.Column(db.String(50))

    risk_score = db.Column(db.Integer)
    risk_level = db.Column(db.String(20))
    action = db.Column(db.String(200))
    ai_explanation = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ✅ INIT DB AFTER MODELS (VERY IMPORTANT)
init_db(app)

# ---------------- ROUTES ----------------
@app.route('/')
def home():
    return render_template("home.html")


# ---------------- REGISTER ----------------
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        existing = User.query.filter_by(username=username).first()
        if existing:
            return render_template("register.html", error="User already exists")

        user = User()
        user.username = username
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route('/login', methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            session["role"] = user.role

            if user.role == "doctor":
                return redirect(url_for("doctor_dashboard"))

            return redirect(url_for("analyze"))

        error = "Invalid username or password"

    return render_template("login.html", error=error)


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- PATIENT ----------------
@app.route('/analyze', methods=["GET", "POST"])
def analyze():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        data = request.form

        risk = ai_agent(data)

        record = PatientRecord()
        record.user_id = session["user_id"]
        record.symptoms = data.get("symptoms")
        record.severity = data.get("severity")
        record.duration = int(data.get("duration", 0))
        record.age = int(data.get("age", 0))
        record.bp = data.get("bp")

        # ✅ SAFE SPO2
        record.spo2 = int(data.get("spo2", 0)) if data.get("spo2") else None

        record.sugar = int(data.get("sugar", 0))
        record.pain = int(data.get("pain", 0))
        record.city = data.get("city")

        record.risk_score = risk["score"]
        record.risk_level = risk["level"]
        record.action = risk["action"]
        record.ai_explanation = risk["explanation"]

        db.session.add(record)
        db.session.commit()

        socketio.emit("new_case", {
            "risk": risk["level"],
            "city": data.get("city")
        })

        return render_template("result.html", result=record)

    return render_template("analyze.html")


# ---------------- HISTORY ----------------
@app.route('/history')
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))

    records = PatientRecord.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template("timeline.html", records=records)


# ---------------- DOCTOR ----------------
@app.route('/doctor')
def doctor_dashboard():
    if session.get("role") != "doctor":
        return redirect(url_for("login"))

    records = PatientRecord.query.order_by(
        PatientRecord.created_at.desc()
    ).all()

    return render_template("doctor_dashboard.html", records=records)


# ---------------- AI LOGIC ----------------
def ai_agent(data):
    score = 0

    if data.get("severity") == "high":
        score += 40
    elif data.get("severity") == "medium":
        score += 20

    if int(data.get("duration", 0)) > 3:
        score += 10

    if int(data.get("age", 0)) > 60:
        score += 15

    if data.get("spo2") and int(data.get("spo2")) < 90:
        score += 30

    if int(data.get("pain", 0)) > 7:
        score += 10

    if score >= 70:
        level = "CRITICAL"
        action = "Emergency care required"
    elif score >= 40:
        level = "MODERATE"
        action = "Doctor consultation required"
    else:
        level = "LOW"
        action = "Self care"

    return {
        "score": score,
        "level": level,
        "action": action,
        "explanation": f"Risk calculated. Score={score}"
    }


# ---------------- SOCKET ----------------
@socketio.on("connect")
def connect():
    emit("connected", {"msg": "Connected"})


# ---------------- RUN ----------------
if __name__ == "__main__":
    socketio.run(app, debug=True)