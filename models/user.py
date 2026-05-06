from typing import Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash
from db import db


class User(db.Model):  # type: ignore
    __tablename__ = "users"

    # =========================
    # Database Fields
    # =========================
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="patient")
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Optional (use later)
    specialization = db.Column(db.String(100), nullable=True)  # for doctors
    location = db.Column(db.String(120), nullable=True)        # city/area

    # =========================
    # Constructor
    # =========================
    def __init__(
        self,
        username: str,
        password: str,
        role: str = "patient",
        specialization: str | None = None,
        location: str | None = None
    ) -> None:
        self.username = username.strip().lower()
        self.set_password(password)
        self.role = role
        self.specialization = specialization
        self.location = location

    # =========================
    # Password Handling
    # =========================
    def set_password(self, password: str) -> None:
        """Hash and store password securely"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        return check_password_hash(self.password_hash, password)

    # =========================
    # Role Helpers
    # =========================
    def is_admin(self) -> bool:
        return self.role == "admin"

    def is_doctor(self) -> bool:
        return self.role == "doctor"

    def is_patient(self) -> bool:
        return self.role == "patient"

    # =========================
    # Serialization
    # =========================
    def to_dict(self) -> Dict[str, Any]:
        """Safe JSON serialization (no password exposure)"""
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "specialization": self.specialization,
            "location": self.location,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    # =========================
    # Debug Representation
    # =========================
    def __repr__(self) -> str:
        return f"<User {self.username} ({self.role})>"
