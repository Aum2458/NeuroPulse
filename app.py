import os
from datetime import datetime
from dotenv import load_dotenv

from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, emit

from db import db, init_db, User

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- APP SETUP ----------------
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "safe_dev_key")

# ---------------- DATABASE ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///neuro_pulse_v3.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ---------------- SOCKET IO (RENDER SAFE) ----------------
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)

# ---------------- INIT DB ----------------
init_db(app)

# ---------------- MODEL ----------------
class PatientRecord(db.Model):
    __tablename__ = "patient_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    symptoms = db.Column(db.String(200))
    severity = db.Column(db.String(20))
    duration = db.Column(db.Integer)
    age = db.Column(db.Integer)
    bp = db.Column(db.String(20))
    spo2 = db.Column(db.Integer, nullable=True)

    sugar = db.Column(db.Integer)
    pain = db.Column(db.Integer)
    city = db.Column(db.String(50))

    risk_score = db.Column(db.Integer)
    risk_level = db.Column(db.String(20))
    action = db.Column(db.String(200))
    ai_explanation = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if User.query.filter_by(username=username).first():
            return render_template("register.html", error="User already exists")

        user = User()
        user.username = username
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            session["role"] = user.role

            return redirect(
                url_for("doctor_dashboard")
                if user.role == "doctor"
                else url_for("analyze")
            )

        error = "Invalid username or password"

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- AI ENGINE ----------------
def ai_agent(data):
    score = 0

    severity = data.get("severity")
    if severity == "high":
        score += 40
    elif severity == "medium":
        score += 20

    duration = int(data.get("duration") or 0)
    age = int(data.get("age") or 0)
    pain = int(data.get("pain") or 0)

    if duration > 3:
        score += 10

    if age > 60:
        score += 15

    spo2_val = data.get("spo2")
    if spo2_val is not None and str(spo2_val).isdigit():
        if int(spo2_val) < 90:
            score += 30

    if pain > 7:
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


# ---------------- ANALYZE ----------------
@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        data = request.form
        risk = ai_agent(data)

        # SAFE INT CONVERSION (fixes Pylance + crashes)
        def to_int(value):
            try:
                return int(value)
            except:
                return 0

        record = PatientRecord(
            user_id=session.get("user_id"),
            symptoms=data.get("symptoms"),
            severity=data.get("severity"),
            duration=to_int(data.get("duration")),
            age=to_int(data.get("age")),
            bp=data.get("bp"),
            spo2=to_int(data.get("spo2")) if data.get("spo2") else None,
            sugar=to_int(data.get("sugar")),
            pain=to_int(data.get("pain")),
            city=data.get("city"),
            risk_score=risk["score"],
            risk_level=risk["level"],
            action=risk["action"],
            ai_explanation=risk["explanation"]
        )

        db.session.add(record)
        db.session.commit()

        socketio.emit("new_case", {
            "risk": risk["level"],
            "city": data.get("city")
        })

        return render_template("result.html", result=record)

    return render_template("analyze.html")


@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))

    records = PatientRecord.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template("timeline.html", records=records)


@app.route("/doctor")
def doctor_dashboard():
    if session.get("role") != "doctor":
        return redirect(url_for("login"))

    records = PatientRecord.query.order_by(
        PatientRecord.created_at.desc()
    ).all()

    return render_template("doctor_dashboard.html", records=records)


# ---------------- SOCKET ----------------
@socketio.on("connect")
def connect():
    emit("connected", {"msg": "Connected"})


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)