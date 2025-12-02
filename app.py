from flask import (
    Flask, render_template, request,
    jsonify, session, redirect, url_for, abort
)
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "change-this-secret-key"   # koi random string rakh lena

DB_NAME = "users.db"

# ---------- USER DATABASE BANANA ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- PAGES ----------
@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login_page"))

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    # yahan tum apna dashboard.html use kar rahi ho
    return render_template("dashboard.html", user_name=session.get("user_name"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

# ---------- SIGNUP API ----------
@app.route("/api/signup", methods=["POST"])
def api_signup():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"ok": False, "message": "All fields are required."}), 400

    password_hash = generate_password_hash(password)

    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?,?,?)",
            (name, email, password_hash),
        )
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        return jsonify({"ok": False, "message": "Email already registered."}), 400

    return jsonify({"ok": True, "message": "Signup successful. Please login."})

# ---------- LOGIN API ----------
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"ok": False, "message": "Email and password are required."}), 400

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, name, password_hash FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"ok": False, "message": "Invalid email or password."}), 401

    user_id, name, pwd_hash = row

    if not check_password_hash(pwd_hash, password):
        return jsonify({"ok": False, "message": "Invalid email or password."}), 401

    # login success
    session["user_id"] = user_id
    session["user_name"] = name
    return jsonify({"ok": True, "message": "Login successful."})

if _name_ == "_main_":
    app.run(debug=True)

