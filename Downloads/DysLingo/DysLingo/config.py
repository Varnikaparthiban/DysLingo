import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("DYSLINGO_SECRET_KEY", "change-this-development-key")
    DATABASE = os.path.join(BASE_DIR, "dyslingo.db")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
