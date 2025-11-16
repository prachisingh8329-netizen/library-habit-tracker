import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__, template_folder="templates", static_folder="static")

# Secret key for sessions: use env var in Render (optional)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-for-local")  # set SECRET_KEY in Render for security

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_FILE = os.path.join(DATA_DIR, "users.json")
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, indent=2)

def read_users():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def write_users(users):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

# ----- Routes (pages) -----
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard_page():
    if not session.get("user_email"):
        return redirect(url_for("login_page"))
    # send dashboard with session user name available
    return render_template("dashboard.html", user_name=session.get("user_name"))

@app.route("/scan-book")
def scan_book_page():
    if not session.get("user_email"):
        return redirect(url_for("login_page"))
    return render_template("scan_book.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ----- API endpoints -----
@app.route("/api/signup", methods=["POST"])
def api_signup():
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    users = read_users()
    if any(u.get("email") == email for u in users):
        return jsonify({"message": "User already exists"}), 400

    users.append({"name": name, "email": email, "password": password})
    write_users(users)
    return jsonify({"message": "Signup successful", "user": {"name": name, "email": email}}), 200

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    users = read_users()
    user = next((u for u in users if u["email"] == email and u["password"] == password), None)
    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    # set session
    session["user_email"] = user["email"]
    session["user_name"] = user.get("name", "")
    return jsonify({"message": "Login successful", "user": {"name": user.get("name"), "email": user.get("email")}}), 200

# simple health check
@app.route("/ping")
def ping():
    return "pong"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
