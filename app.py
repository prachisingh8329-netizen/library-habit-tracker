from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "my-secret-key-123"

DB_NAME = "users.db"

# ---------------- DATABASE CREATE ----------------
def create_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

create_db()

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    if "user_id" in session:
        return redirect("/dashboard")
    return redirect("/login")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html", username=session.get("username"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- API: SIGNUP ----------------
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"success": False, "message": "All fields required"})

    password_hash = generate_password_hash(password)

    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (?,?,?)",
                    (name, email, password_hash))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Signup success"})
    except:
        return jsonify({"success": False, "message": "Email already exists"})

# ---------------- API: LOGIN ----------------
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id,name,password FROM users WHERE email=?", (email,))
    user = cur.fetchone()
    conn.close()

    if not user:
        return jsonify({"success": False, "message": "Invalid email or password"})

    if not check_password_hash(user[2], password):
        return jsonify({"success": False, "message": "Wrong password"})

    session["user_id"] = user[0]
    session["username"] = user[1]

    return jsonify({"success": True})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)

