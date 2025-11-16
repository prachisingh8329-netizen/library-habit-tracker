from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from flask_cors import CORS
import os, json

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

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

# ---- Pages ----
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup-page")
def signup_page():
    return render_template("signup.html")

@app.route("/login-page")
def login_page():
    return render_template("sign.html")

@app.route("/dashboard")
def dashboard_page():
    # In real app you'd check session; here we just render dashboard
    return render_template("dashboard.html")

@app.route("/scan-book")
def scan_book_page():
    return render_template("scan_book.html")

# ---- API ----
@app.route("/api/signup", methods=["POST"])
def api_signup():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"message":"All fields required"}), 400

    users = read_users()
    if any(u.get("email") == email for u in users):
        return jsonify({"message":"User already exists"}), 400

    users.append({"name":name, "email":email, "password":password})
    write_users(users)
    return jsonify({"message":"Signup successful", "user":{"name":name, "email":email}})

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    users = read_users()
    user = next((u for u in users if u["email"]==email and u["password"]==password), None)
    if not user:
        return jsonify({"message":"Invalid credentials"}), 401

    # NOTE: not using sessions for simplicity; in prod use flask-login or JWT
    return jsonify({"message":"Login successful", "user":{"name":user["name"], "email":user["email"]}})

# Serve static files if needed (CSS/JS)
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
