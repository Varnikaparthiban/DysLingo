from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from config import Config
from utils.db import init_db, get_db
from utils.text_processing import analyze_reading
from utils.ocr import extract_text_from_image
from models.risk_screening import score_screening

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True) if False else None
init_db()

@app.route("/")
def index():
    db = get_db()
    sessions = db.execute("SELECT * FROM sessions ORDER BY created_at DESC LIMIT 5").fetchall()
    totals = db.execute("SELECT COUNT(*) AS n, COALESCE(AVG(accuracy),0) AS accuracy, COALESCE(AVG(wpm),0) AS wpm FROM sessions").fetchone()
    return render_template("index.html", sessions=sessions, totals=totals)

@app.route("/reader", methods=["GET", "POST"])
def reader():
    extracted_text = ""
    if request.method == "POST":
        uploaded = request.files.get("image")
        if uploaded and uploaded.filename:
            try:
                extracted_text = extract_text_from_image(uploaded)
            except RuntimeError as exc:
                flash(str(exc), "warning")
            except Exception:
                flash("Could not read that image. Try a clearer JPG or PNG image.", "warning")
        else:
            extracted_text = request.form.get("text", "")
    return render_template("reader.html", extracted_text=extracted_text)

@app.route("/practice", methods=["GET", "POST"])
def practice():
    result = None
    if request.method == "POST":
        target = request.form.get("target_text", "").strip()
        spoken = request.form.get("spoken_text", "").strip()
        language = request.form.get("language", "en-US")
        if target and spoken:
            result = analyze_reading(target, spoken)
            db = get_db()
            db.execute(
                "INSERT INTO sessions (language, target_text, spoken_text, accuracy, wpm, errors, pauses, duration_seconds) VALUES (?,?,?,?,?,?,?,?)",
                (language, target, spoken, result["accuracy"], result["wpm"], result["errors"], result["pauses"], result["duration_seconds"])
            )
            db.commit()
            flash("Practice session saved to your progress history.", "success")
        else:
            flash("Enter the passage and the recognized/spoken text to analyze.", "warning")
    return render_template("practice.html", result=result)

@app.route("/screening", methods=["GET", "POST"])
def screening():
    result = None
    if request.method == "POST":
        answers = {}
        for key in ["q1", "q2", "q3", "q4", "q5", "q6"]:
            try:
                answers[key] = int(request.form.get(key, "0"))
            except ValueError:
                answers[key] = 0
        result = score_screening(answers)
    return render_template("screening.html", result=result)

@app.route("/analytics")
def analytics():
    db = get_db()
    sessions = db.execute("SELECT * FROM sessions ORDER BY created_at DESC").fetchall()
    return render_template("analytics.html", sessions=sessions)

@app.route("/teacher")
def teacher():
    db = get_db()
    sessions = db.execute("SELECT * FROM sessions ORDER BY created_at DESC").fetchall()
    summary = db.execute("SELECT COUNT(*) AS n, COALESCE(AVG(accuracy),0) AS accuracy, COALESCE(AVG(wpm),0) AS wpm FROM sessions").fetchone()
    return render_template("teacher.html", sessions=sessions, summary=summary)

@app.route("/api/session/<int:session_id>")
def session_detail(session_id):
    db = get_db()
    row = db.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Session not found"}), 404
    return jsonify(dict(row))

if __name__ == "__main__":
    app.run(debug=True)
