# db.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------- DATABASE INIT --------------------
db = SQLAlchemy()

def init_db(app):
    """
    Initialize the database with the Flask app context.
    Call this in app.py after app is created.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()

# -------------------- USER MODEL --------------------
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    role = db.Column(db.String(50), default='patient')  # patient, doctor, admin
    city = db.Column(db.String(100), nullable=True)  # User location
    baseline_hr = db.Column(db.Float, default=70)  # User baseline heart rate
    baseline_spo2 = db.Column(db.Float, default=98)  # User baseline oxygen
    conditions = db.Column(db.String(255), default="")  # comma-separated conditions
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str):
        """Hashes and stores the password securely."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifies the provided password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def add_condition(self, condition: str):
        """Add a health condition to user profile."""
        cond_list = [c.strip() for c in self.conditions.split(",") if c.strip()]
        if condition not in cond_list:
            cond_list.append(condition)
        self.conditions = ",".join(cond_list)

    def remove_condition(self, condition: str):
        """Remove a health condition."""
        cond_list = [c.strip() for c in self.conditions.split(",") if c.strip()]
        if condition in cond_list:
            cond_list.remove(condition)
        self.conditions = ",".join(cond_list)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"

# -------------------- TIMELINE MODEL --------------------
class Timeline(db.Model):
    __tablename__ = 'timeline'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    symptoms = db.Column(db.String(500), nullable=False)
    risk_level = db.Column(db.String(50), nullable=False)
    risk_score = db.Column(db.Float, nullable=False)
    ai_explanation = db.Column(db.String(1000), nullable=True)

    user = db.relationship('User', backref=db.backref('timelines', lazy=True))

    def __repr__(self):
        return f"<Timeline User:{self.user_id} Risk:{self.risk_level} Time:{self.timestamp}>"

# -------------------- EXAMPLE USAGE --------------------
# You can import db, User, Timeline, and init_db in your app.py like this:
# from db import db, init_db, User, Timeline
