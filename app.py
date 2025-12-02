from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# -------- DATABASE CONNECTION ----------
def get_db():
    return sqlite3.connect("users.db")

# -------- CREATE TABLE IF NOT EXISTS ----------
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# -------- HOME REDIRECT ----------
@app.route("/")
def home():
    return redirect("/login")

# -------- SIGNUP ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    message = ""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email").lower()
        password = request.form.get("password")

        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)",
                        (name, email, password))
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            message = "Email already exists!"

    return render_template("signup.html", message=message)

# -------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        email = request.form.get("email").lower()
        password = request.form.get("password")

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id,name,password FROM users WHERE email=?", (email,))
        user = cur.fetchone()
        conn.close()

        if user and user[2] == password:
            session["user"] = user[1]
            return redirect("/dashboard")
        else:
            message = "Invalid Email or Password!"

    return render_template("login.html", message=message)

# -------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", user=session["user"])

# -------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ✅ IMPORTANT FIX FOR YOUR ERROR
if __name__ == "__main__":
    app.run(debug=True)
