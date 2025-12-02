from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "change-this-key-123"  # random string rakh sakti ho

# ---------- DATABASE SETUP ----------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "auth.db")  # NEW DB, purane mess se alag


def get_db():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


init_db()

# ---------- PAGES ----------
@app.route("/")
def index():
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
    # yahan tumhara existing dashboard.html use hoga
    return render_template("dashboard.html", username=session.get("username"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))


# ---------- SIGNUP API ----------
@app.route("/api/signup", methods=["POST"])
def api_signup():
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not name or not email or not password:
        return jsonify({"success": False, "message": "Please fill all fields."}), 400

    password_hash = generate_password_hash(password)

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?,?,?)",
            (name, email, password_hash),
        )
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        return jsonify(
            {"success": False, "message": "This email is already registered."}
        ), 400

    return jsonify({"success": True, "message": "Signup successful. Please login."})


# ---------- LOGIN API ----------
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify(
            {"success": False, "message": "Enter email and password."}
        ), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, password_hash FROM users WHERE email = ?", (email,)
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify(
            {"success": False, "message": "Invalid email or password."}
        ), 401

    user_id, name, password_hash = row

    if not check_password_hash(password_hash, password):
        return jsonify(
            {"success": False, "message": "Invalid email or password."}
        ), 401

    session["user_id"] = user_id
    session["username"] = name
    return jsonify({"success": True, "message": "Login successful."})


if __name_ == "__main__":
    app.run(debug=True)
