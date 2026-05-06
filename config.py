import os

class Config:
    """
    Central configuration for the Flask app.
    """
    # ---------------- Security ----------------
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'replace-this-secret-key')

    # ---------------- Database ----------------
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///neuro_pulse.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ---------------- Uploads ----------------
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit

    # ---------------- Environment ----------------
    DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'

    # ---------------- AI / External APIs ----------------
    AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")  # 'gemini' or 'openai'
    OPENAI_API_KEY = os.getenv("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", "")
    GEMINI_API_KEY = os.getenv("AIzaSyAeqDVomSSB7s--lz_fPJsJ_9MMIeHvMww", "")
